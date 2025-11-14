import view
import model

def control(user, view_name, **kwargs):
    permissions = {"Bank manager": 0,
                   "Customer": 1,
                   "Data analyst": 2}

    df = model.dataset_crafting()
    model.daily_to_monthly()
    model.insert_noise()
    model.daily_entries_2_to_monthly()

    view_name(df, **kwargs)
    customer = kwargs.get("customer",None)

    print(view.get_data(df, permissions[user], name=customer))

    

