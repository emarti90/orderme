# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# import General Packages
import unittest

# Import User Packages
from user.test import UserTest
from menu.test import MenuTest
from order.test import OrderTest

if __name__ == '__main__':
    unittest.main()