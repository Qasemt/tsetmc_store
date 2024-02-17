
import threading
import tsetmc
 

if __name__ == "__main__":
   
    lock = threading.Lock()
    wait_list = list()
    complete_list = list()
    running_list = list()
    fail_list = list()
   
    a = tsetmc.SyncTsetmc(id=id,lock=lock, wait_list=wait_list, complete_list=complete_list, running_list=running_list,
               fail_list=fail_list)
    tsetmc_ids,data_in_csv_file = a.load_csv()
    
    # 26014913469567886 vaghadir
    # 15917865009187760 مادیرا
    b1,e= a.get_share_info(15917865009187760)

    a.collect_all_shares_info(tsetmc_ids= tsetmc_ids,data_in_csv_file=data_in_csv_file)

    a.saveCSV()
 