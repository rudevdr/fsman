idcs = []
didc = None

def get_idcs():
    return idcs

def add_didc(idc):
    global didc
    didc = idc

def add_idc(idc):
    idcs.append(idc)

def remove_idc(idc):
    idcs.remove(idc)

def clear_idcs():
    idcs.clear()

def get_idc_obj(idc):
    return idc.current_obj

def get_idc_index(idc):
    return idc.current_index

def get_didc_obj():
    if didc:
        return get_idc_obj(didc)

def get_didc_index():
    if didc:
        return get_idc_index(didc)

def get_all_unique_idcs():
    return list(set(idcs+didc))

def get_all_obj():
    didc_obj = get_didc_obj()
    idcs_obj = get_idcs_obj()
    if didc_obj in get_idcs_obj():
        return idcs_obj
    else:
        return idcs_obj + [didc_obj]

def get_idcs_obj():
    return [get_idc_obj(idc) for idc in get_idcs()]

def get_idcs_index():
    return [get_idc_index(idc) for idc in get_idcs()]

def get_idc_from_index(index):
    return [idc for idc in get_idcs() if get_idc_index(idc) == index][0]

def move_didc_up():
    didc.move_up()

def move_didc_down():
    didc.move_down()

def toggle_idc(idc):
    index = get_didc_index()
    if index in get_idcs_index():
        idc = get_idc_from_index(index)
        idc.delete_idc()
        remove_idc(idc)
    else:
        add_idc(idc)
    didc.move_to_top()
