import unittest
from home_work2 import function_that_says_ni 
 
class TestFunctionThatSaysNi(unittest.TestCase):
    
    def test_valid_bushes_with_cost(self):
        self.assertEqual(function_that_says_ni({"name": "храст", "cost": 1.50}, {"name": "sHRub", "cost": 3.00}), "4.50лв")
        self.assertEqual(function_that_says_ni({"name": "хРАст", "cost": 150}, {"name": "shrub", "cost": 3.00}), "Ni!")
 
    def test_invalid_bushes(self):
        self.assertEqual(function_that_says_ni({"ddd": "храст", "cost": 1.50}, {"namae": "sHRub", "cost": 3.00}), "Ni!")
        self.assertEqual(function_that_says_ni({"namdde": "хРАст", "cost": 150}, {"namse": "shrub", "cost": 3.00}), "Ni!")
 
    def test_invalid_bushes_with_cost(self):
        self.assertEqual(function_that_says_ni({"name": "буш", "cost": 1.00}, {"name": "храст", "cost": 244.00}), "Ni!")
        self.assertEqual(function_that_says_ni({"name": "буш", "cost": 1.00}, {"name": "храстченце", "cost": 2.00}), "Ni!")
        self.assertEqual(function_that_says_ni({"name": "буш", "cost": 1.00}, {"name": "храст", "cost": 41.99}), "41.99лв")
 
    def test_valid_bushes_without_cost(self):
        self.assertEqual(function_that_says_ni({"name": "храст"}, {"name": "buSh"}), "Ni!")
        self.assertEqual(function_that_says_ni(a={"name": "храст"}, b={"name": "shrub"}), "Ni!")
 
    def test_invalid_bushes_without_cost(self):
        self.assertEqual(function_that_says_ni({"name": "храст44"}, {"name": "bus44h"}), "Ni!")
        self.assertEqual(function_that_says_ni(a={"name": "храс124т"}, b={"name": "s52hrub"}), "Ni!")
 
    def test_valid_bushes_with_and_without_cost(self):
        self.assertEqual(function_that_says_ni({"name": "храст"}, {"name": "bush", "cost": 33.33}), "33.33лв")
        self.assertEqual(function_that_says_ni(a={"name": "храст", "cost": 17}, b={"name": "shrub"}), "Ni!")
 
    def test_not_pretty_bushes_due_to_price(self):
        self.assertEqual(function_that_says_ni({"name": "храсТ", "cost": 50.0}), "Ni!")
        self.assertEqual(function_that_says_ni({"name": "shrub", "cost": 43.00}), "Ni!")
 
    def test_not_pretty_bushes_due_to_unique_letters(self):
        self.assertEqual(function_that_says_ni(ad={"name": "храст", "cost": 1.80}, b={"name": "храст", "cost": 1}), "Ni!")
        self.assertEqual(function_that_says_ni(a={"name": "буш"}, b={"name": "шрасх"}), "Ni!")
 
    def test_mixed_types(self):
       self.assertEqual(function_that_says_ni(4, 4, {"name": "храст", "cost": 0.0}, [3,4,5], ad={"name": "храст", "cost": 1.80}), "1.80лв")
       self.assertEqual(function_that_says_ni(4, 4, {"name": "храст", "cost": 30.0}, [3,4,5], ad={"name": "храст", "cost": 1.80}), "Ni!")
       self.assertEqual(function_that_says_ni(4, 4, {"name": "храст", "cost": 40.0}, [3,4,5], ad={"name": "храст", "cost": 1.80}), "Ni!")  
       self.assertEqual(function_that_says_ni(4, 4, {"name": "храст", "cost": 40.0}, [3,4,5], ad={"name": "храст", "cost": 1.80}, da=(1,2)), "Ni!")  
       self.assertEqual(function_that_says_ni({"name": "храст"}, {"name": "храст", "cost": 0.0}, ["ffffffffff", {1, 2, 3}]), "Ni!") 
    
    def test_all_in_one_first_variation(self):
       self.assertEqual(function_that_says_ni(4, 4, {"name": "ХРраст", "cost": 10.0}, [3,4,5], ad={"name": "хРаст", "cost": 1.80}, da = "pypy"), "1.80лв")
       self.assertEqual(function_that_says_ni(4, 4, {"name": "Храст", "cost": 100.0}, ad={"name": "дърво", "cost": 1.80}, c = "pypy"), "Ni!")
       self.assertEqual(function_that_says_ni( {"name": "Храст", "cost": 100.0}, ad={"name": "дърво", "cost": 1.80}, c = "pypy"), "Ni!")
 
    def test_all_in_one_second_variation(self):
       self.assertEqual(function_that_says_ni( {"name": "Храст", "cost": 11.0}, ad={"name": "дърво", "cost": 1.80}, c = "pypy"), "11.00лв")
       self.assertEqual(function_that_says_ni( {"name": "Храст", "cost": 11.0}, ad={"name": "bush", "cost": 1.80}, c = "pypy"), "Ni!")
       self.assertEqual(function_that_says_ni( {"name": "Храст", "cost": 12.0}, ad={"name": "дърво", "cost": 1.80}, c = "pypy"), "12.00лв")
        
if __name__ == '__main__':
    unittest.main()