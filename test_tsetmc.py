import unittest
import tsetmc
import threading

class TestShareInfo(unittest.TestCase):
    def setUp(self):
        lock = threading.Lock()
        wait_list = list()
        complete_list = list()
        running_list = list()
        fail_list = list()
   
        self.a = tsetmc.SyncTsetmc(id=id,lock=lock, wait_list=wait_list, complete_list=complete_list, running_list=running_list,
               fail_list=fail_list)
 
    def test_nemad_farabource(self):
        company, e = self.a.get_share_info(15917865009187760)
        self.assertEqual(company['exchange_code'], 3) # exchange farabource
        self.assertEqual(e, None)

    def test_nemad_bource(self):
        company, e = self.a.get_share_info(26014913469567886)
        self.assertEqual(company['exchange_code'], 2) # exchange bource
        self.assertEqual(e, None)

 

if __name__ == '__main__':
    unittest.main()