import os
import requests
import ast
import threading
import csv


class My_Response:
    status_code = 0
    error = ""

    def Status_code(self, code):
        self.status_code = code

    def Error(self, error):
        self.error = error


class SyncTsetmc:

    def __init__(
        self,
        id,
        lock,
        wait_list,
        complete_list,
        running_list,
        fail_list,
    ):
        self.id = id
        self.wait_list = wait_list
        self.complete_list = complete_list
        self.running_list = running_list
        self.fail_list = fail_list
        self.lock = lock
        self.tsetmc_base_url = "http://old.tsetmc.com/Loader.aspx"
        self.request_obj = requests
        self.request_obj_timeout = (100, 180)
        self.result_stock = []

        self.bourse_index = 32097828799138957
        self.farabourse_index = 43685683301327984
        self.csv_file_path = "data.csv"
        # -------------------
        self.print_color = "green"

    def print_c(self, text, color=None):
        print(text)

    def get_var_list(self, response, var_name):
        # -----------------------------------------------------------------------
        # error_codes:
        # -1 ==> no error
        # 2001 ==> error on get_var_list function: cant find start position
        # 2002 ==> error on get_var_list function: cant find end position
        # 2003 ==> error on get_var_list function: much long list
        # 2004 ==> error on get_var_list function: get_var_list another error
        # -----------------------------------------------------------------------

        # fins start position
        start_pos = response.text.find(var_name)
        if start_pos < 0:
            result = False
            error = "cant find start position"
            error_code = 2001
            return result, error, error_code

        start_pos += len(var_name)

        # fins end position
        end_pos = response.text.find(";", start_pos)
        if end_pos < 0:
            result = False
            error = "cant find end position"
            error_code = 2002
            return result, error, error_code

        # if result is True:
        var_str = str(response.text[start_pos:end_pos])
        if len(var_str) > 1000000000:
            result = False
            error = "cant get list: much long list: {}".format(len(var_str))
            error_code = 2003
            return result, error, error_code

        try:
            # self.print_c('{3}  start_pos:{0}  end_pos:{1}  var_str_len:{2}'.format(start_pos, end_pos, len(var_str), var_name))
            var_list = ast.literal_eval(var_str)
            result = var_list
            error = None
            error_code = -1
        except Exception as e:
            result = False
            error = "get_var_list error: {0}".format(str(e))
            error_code = 2004
        return result, error, error_code

    def get_web_data(self, url, timeout=None):
        try:
            if timeout is None:
                return self.request_obj.get(url, timeout=self.request_obj_timeout)
                # return self.request_obj.get(url, headers=self.request_obj_header, timeout=self.request_obj_timeout)
            else:
                return self.request_obj.get(url, timeout=timeout)
                # return self.request_obj.get(url, headers=self.request_obj_header, timeout=timeout)
        except Exception as e:
            a = My_Response()
            a.Status_code(100)
            a.Error(e)
            return a

        # return response
        # if response.status_code == 200:
        #    return True, response
        # else:
        #    return False, response

    def get_share_info(self, share_id):  # کرفتن اطلاعات سهام
        error = None
        url = "{0}?Partree=15131M&i={1}".format(self.tsetmc_base_url, share_id)
        response = self.get_web_data(url)

        # check response code
        if response.status_code != 200:
            error = "html error code:{0}".format(response.status_code)
            result = False
            return result, error

        # -------------------
        result = dict()
        start_pos = 0
        end_pos = 0
        offset = 0
        td_list = list()
        while start_pos >= 0 and end_pos >= 0:
            start_pos = response.text.find("<td>", offset)
            if start_pos < 0:
                continue
            start_pos += 4  # len(var_name)

            # fins end position
            end_pos = response.text.find("</td>", start_pos)
            if end_pos < 0:
                continue

            try:
                var_str = str(response.text[start_pos:end_pos])
                td_list.append(var_str)
            except Exception as e:
                error = str(e)
                result = False
                return result, error
            offset = end_pos

        try:
            result["en_symbol_12_digit_code"] = str(td_list[1])  # 'کد 12 رقمی نماد'
            result["en_symbol_5_digit_code"] = str(td_list[3])  # 'کد 5 رقمی نماد'
            result["company_en_name"] = str(td_list[5])  # 'نام لاتین شرکت'
            result["company_4_digit_code"] = str(td_list[7])  # 'کد 4 رقمی شرکت'
            result["company_fa_name"] = str(td_list[9])  # 'نام شرکت'
            result["fa_symbol_name"] = str(td_list[11])  # 'نماد فارسی'
            result["fa_symbol_30_digit_code"] = str(td_list[13])  # 'نماد 30 رقمی فارسی'
            result["company_12_digit_code"] = str(td_list[15])  # 'کد 12 رقمی شرکت'
            result["market_flow"] = str(td_list[17])  # 'بازار'
            result["bord_code"] = int(td_list[19])  # 'کد تابلو'
            result["industry_code"] = int(td_list[21])  # 'کد گروه صنعت'
            result["sub_industry_code"] = int(td_list[25])  # 'کد زیر گروه صنعت'
            result["group_name"] = str(td_list[23])
            if "فرابورس" in str(td_list[17]):
              result["exchange_code"] = 3  # farbourse
            else:
               result["exchange_code"] = 2 # tehran

            result["group_name"] = str(td_list[23])
            result["is_active"] = 1

        except Exception as e:
            error = str(e)
            result = False
            return result, error

        return result, error

    def get_shares_in_index(self, index_id, tsetmc_ids):
        error = None
        url = "{0}?ParTree=15131J&i={1}".format(self.tsetmc_base_url, index_id)
        response = self.get_web_data(url)
        # check response code
        if response.status_code != 200:
            error = "html error code:{0}".format(response.status_code)
            result = False
            return result, error
        # -------------------
        start_pos = 0
        end_pos = 0
        offset = 0
        id_list = list()
        while start_pos >= 0 and end_pos >= 0:
            start_pos = response.text.find("<tr id='", offset)
            if start_pos < 0:
                continue
            start_pos += 8  # len(var_name)
            # fins end position
            end_pos = response.text.find("'>", start_pos)
            if end_pos < 0:
                continue
            try:
                var_str = str(response.text[start_pos:end_pos])
                var_id = int(var_str)
                if var_str not in tsetmc_ids:
                    id_list.append(var_id)

            finally:
                offset = end_pos
        return id_list, error

    def get_all_related_companies_id(self, share_id):  # کرفتن لیست سهام های هم گروه
        error = None
        url = "{0}?ParTree=151311&i={1}".format(self.tsetmc_base_url, share_id)
        response = self.get_web_data(url)

        # check response code
        if response.status_code != 200:
            error = "html error code:{0}".format(response.status_code)
            result = False
            return result, error

        # -------------------
        var_name = "var RelatedCompanies="  # ---- شرکتهای هم گروه ----
        related_companies, related_companies_error, v = self.get_var_list(response, var_name)
        if related_companies_error is not None:
            error = related_companies_error
            result = False
            return result, error
        share_id_list = list()
        for item in related_companies:
            try:
                share_id_list.append(int(item[0]))
            except Exception as e:
                error = str(e)
                break

        return share_id_list, error

    def collect_all_shares_info(self, tsetmc_ids, data_in_csv_file):
        self.unreade_page = list()
        self.running_page = list()
        self.readed_page = list()
        self.fail_readed_page = list()
        self.result_stock.extend(data_in_csv_file)

        bourse, bourse_error = self.get_shares_in_index(self.bourse_index, tsetmc_ids)
        farabourse, farabourse_error = self.get_shares_in_index(self.farabourse_index, tsetmc_ids)

        if bourse_error is None:
            for share_id in bourse:
                self.unreade_page.append(int(share_id))

        if farabourse_error is None:
            for share_id in farabourse:
                self.unreade_page.append(int(share_id))

        i = 0
        while len(self.unreade_page) != 0:
            i += 1
            share_id = self.unreade_page.pop()
            self.running_page.append(share_id)

            all_related_companies_id, all_related_companies_id_error = self.get_all_related_companies_id(share_id)
            if all_related_companies_id_error is None:
                self.add_share_id_to_unread_page_list(all_related_companies_id)

                share_info, error = self.get_share_info(share_id)
                if error is not None:
                    self.fail_readed_page.append(share_id)
                    self.running_page.remove(share_id)
                    continue

                share_info["tsetmc_id"] = share_id
                # Convert object to a list
                self.result_stock.append(share_info)
                self.readed_page.append(share_id)
                self.running_page.remove(share_id)
                self.print_c("True collect_shares_info: {0} remind: {1} complete: {2}".format(share_id, len(self.unreade_page), i))
                if i > 10:
                    break
            else:
                self.print_c("fail collect_shares_info: {0} remind: {1} complete: {2}".format(share_id, len(self.unreade_page), i))
                self.fail_readed_page.append(share_id)
                self.running_page.remove(share_id)

        # self.browser.close()
        return (self.fail_readed_page, self.running_page, self.unreade_page, self.readed_page)

    def saveCSV(self):
        try:
            # Specify the fieldnames for the CSV file
            fieldnames = self.result_stock[0].keys()

            with open(self.csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()

                writer.writerows(self.result_stock)

        except csv.Error as e:
            print("erro {}".format(e))

    def load_csv(self):
        data_in_csv_file = []
        tsetmc_ids = {}
        try:
            if not os.path.exists(self.csv_file_path):
                open(self.csv_file_path, "w").close()
            with open(self.csv_file_path, "r", encoding="utf-8") as file:

                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    data_in_csv_file.append(row)
                    tsetmc_ids[row["tsetmc_id"]] = row["fa_symbol_name"]
                return tsetmc_ids, data_in_csv_file
        except csv.Error as e:
            return ValueError("load csv{}".format(e))

    def add_share_id_to_unread_page_list(self, id_list):
        try:
            self.lock.acquire()

            for id in id_list:
                if id in self.wait_list:
                    continue
                if id in self.complete_list:
                    continue
                if id in self.running_list:
                    continue
                if id in self.fail_list:
                    continue
                self.wait_list.append(id)
        except:
            self.lock.release()
            return True

        self.lock.release()
        return True
