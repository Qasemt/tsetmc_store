
import threading
import tsetmc
 

if __name__ == "__main__":
   
    
   
    a = tsetmc.SyncTsetmc(id=id )
    tsetmc_ids,data_in_csv_file = a.load_csv()
    
    a.collect_all_shares_info(tsetmc_ids= tsetmc_ids,data_in_csv_file=data_in_csv_file,number_of_read=100)

    a.saveCSV()
 