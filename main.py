
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
    
 

    a.collect_all_shares_info(tsetmc_ids= tsetmc_ids,data_in_csv_file=data_in_csv_file,number_of_read=10)

    a.saveCSV()
 