import pythoncom
from win32com.client import Dispatch, gencache, VARIANT


class KompasAPI:
    def __init__(self):
        #  Подключим описание интерфейсов API7
        self.api7 = gencache.EnsureModule("{69AC2981-37C0-4379-84FD-5DD2F3C0A520}", 0, 1, 0)
        self.application = self.api7.IApplication(
            Dispatch("Kompas.Application.7")._oleobj_.QueryInterface(self.api7.IApplication.CLSID, pythoncom.IID_IDispatch))

        self.kompas_document = self.application.ActiveDocument
        self.kompas_document_3d = self.api7.IKompasDocument3D(self.kompas_document)
        self.part_7 = self.kompas_document_3d.TopPart
        self.property_keeper = self.api7.IPropertyKeeper(self.part_7)
        self.property_mng = self.api7.IPropertyMng(self.application)

    def get_property_value(self, property_name):
        for i in range(self.property_mng.PropertyCount(self.kompas_document)):  # ищем свойство по наименованию
            self.property = self.property_mng.GetProperty(self.kompas_document, i)
            if self.property.Name == property_name:
                self.property_value = self.property_keeper.GetPropertyValue(self.property, "", True, True)
                return self.property_value[1]
        return self.property_value[1]

    def set_property(self, property_name, property_value):
        for i in range(self.property_mng.PropertyCount(self.kompas_document)):
            self.property = self.property_mng.GetProperty(self.kompas_document, i)
            if self.property.Name == property_name:
                self.property_keeper.SetPropertyValue(self.property, property_value, True)
                return self.property
            i += 1

    # Получение значения габаритов детали
    def get_gabarit(self):
        self.model_object = self.api7.IModelObject(self.part_7)
        self.feature_7 = self.model_object.Owner
        self.body_7 = self.feature_7.ResultBodies
        self.bool, self.x_1, self.y_1, self.z_1, self.x_2, self.y_2, self.z_2 = self.body_7.GetGabarit()
        return self.x_2-self.x_1, self.y_2-self.y_1, self.z_2-self.z_1

    # Получение значения массы
    def get_mass(self):
        self.mass_inertia_param_7 = self.api7.IMassInertiaParam7(self.part_7)
        return self.mass_inertia_param_7.Mass

    # Проверка документ на деталь
    def check_part(self):
        if self.kompas_document.DocumentType != 4:
            self.application.MessageBoxEx("Данный макрос работает только с деталью", "Документ не является деталью", 0)
            return False
        return True
