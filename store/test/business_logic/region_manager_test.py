from unittest import TestCase
from store.business_logic import region_manager, validation
from mock import patch


class RegionManagerTest(TestCase):

    def test_validation_region_name_long_name(self):
        name = 'very very very loooooooooooooooooooooooooooooooong name'
        with self.assertRaises(validation.ValidationException):
            region_manager.validationRegionName(name)

    def test_validation_region_without_name(self):
        with self.assertRaises(validation.ValidationException):
            region_manager.validationRegionName(None)

    @patch('business_logic.region_manager.RegionDao.getAllRegions')
    def test_get_region_list(self, m_reg):
        region_manager.getlistRegion()
        self.assertEqual(m_reg.call_count, 1)

    @patch('business_logic.region_manager.validationRegionID')
    @patch('business_logic.region_manager.validationRegionName')
    @patch('business_logic.region_manager.RegionDao.updateRegion')
    def test_update_region(self, m_upd, m_rname, m_rid):
        region_manager.updateRegion('id', 'name')
        self.assertEqual(m_upd.call_count, 1)
        self.assertEqual(m_rname.call_count, 1)
        self.assertEqual(m_rid.call_count, 1)

    @patch('business_logic.region_manager.RegionDao.createNewRegion')
    @patch('business_logic.region_manager.validationRegionName')
    def test_create_region(self, m_val_id, m_cr):
        region_manager.createRegion('name')
        self.assertEqual(m_val_id.call_count, 1)
        self.assertEqual(m_cr.call_count, 1)

    @patch('business_logic.region_manager.RegionDao.deleteRecord')
    @patch('business_logic.region_manager.validationRegionID')
    def test_delete_region(self, m_val_id, m_del):
        region_manager.deleteRegion('id')
        self.assertEqual(m_val_id.call_count, 1)
        self.assertEqual(m_del.call_count, 1)

    @patch('business_logic.region_manager.RegionDao.getRegionByID')
    @patch('business_logic.region_manager.validationRegionID')
    def test_get_region(self, m_val_id, m_get):
        region_manager.getRegionByID('id')
        self.assertEqual(m_val_id.call_count, 1)
        self.assertEqual(m_get.call_count, 1)
