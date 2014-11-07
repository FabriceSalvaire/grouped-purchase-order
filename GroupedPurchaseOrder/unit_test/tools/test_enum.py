####################################################################################################
# 
# @Project@ - @ProjectDescription@.
# Copyright (C) 2014 Fabrice Salvaire
# 
####################################################################################################

####################################################################################################

import unittest

####################################################################################################

from GroupedPurchaseOrder.tools.enum import ChoiceEnum

####################################################################################################

class TestEnum(unittest.TestCase):

    ##############################################

    def test(self):

        def _(x):
            return x

        class OrderStatus(ChoiceEnum):
            new = _('new')
            ordered = _('ordered')
            delivered = _('delivered')

        self.assertEqual(OrderStatus.new.value, 1)
        # self.assertTrue(OrderStatus.new == 1) # don't work = 0
        self.assertEqual(OrderStatus.new.label, 'new')
        self.assertListEqual(OrderStatus.to_list(),
                             [(1, 'new'), (2, 'ordered'), (3, 'delivered')])

####################################################################################################

if __name__ == '__main__':

    unittest.main()

####################################################################################################
# 
# End
# 
####################################################################################################