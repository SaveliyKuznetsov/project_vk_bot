from unittest import TestCase



import main1

from unittest import TestCase
 
 
 
class Test1(TestCase):
    def test_sh1(self):
        self.assertEqual(main1.share(120), (0, 1, 2, 0))
        self.assertEqual(main1.share(674631), (674, 6, 3, 1))
        self.assertEqual(main1.share(452515),(452, 5, 1, 5) )

        

if __name__ == "__main__":
  unittest.main()
  

