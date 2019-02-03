from frappe import _

def get_data():
	return {
		'heatmap': True,
		'heatmap_message': _('This is based on transactions against this Property. See timeline below for details'),
		'fieldname': 'property',
		'transactions': [
			{
				'label': _('Contract'),
				'items': ['Rent Contract']
			},
			{
				'label': _('Receipt'),
				'items': ['Rent Receipt']
			}
		]
	}