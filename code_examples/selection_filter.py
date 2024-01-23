import clr
from pyrevit import HOST_APP

clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference("RevitAPIUI")
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import *

class CustomSelectionFilter(ISelectionFilter):
	def __init__(self, categories):
		#User supplied categories
		self.categories = categories or []
		#Elements selected
		self.elements = []

	def AllowElement(self, element):
		type_match = element.Category.Name in self.categories
		is_unique_element = element.Id not in self.elements
		if (type_match and is_unique_element):
			return True
		else:
			return False
			
	def AllowReference(self, reference, point):
		return False

doc = HOST_APP.doc
uidoc = HOST_APP.uidoc

#Create Custom Selection Filter
selection_filter = CustomSelectionFilter(['Windows'])

#User Message
TaskDialog.Show("Select Elements", "Select Windows. Press ESC when done")
elements_selected = []

#Pick Model Elements
while True:
	try:
		#reference_selection = uidoc.Selection.PickObject(Selection.ObjectType.Element, selection_filter)
		reference_selection = uidoc.Selection.PickObject(ObjectType.Element, selection_filter)
		if reference_selection:
			element_selection = doc.GetElement(reference_selection)
			selection_filter.elements.append(element_selection.Id)
			elements_selected.append(element_selection)
	except Exception as e:
		break

dialog = TaskDialog.Show('Message', str(len(elements_selected)) + ' Elements selected')

