####################################################################################################
# 
# GroupedPurchaseOrder - A Django Application.
# Copyright (C) 2014 Fabrice Salvaire
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
# 
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
