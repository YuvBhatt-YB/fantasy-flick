from datetime import datetime



def convert_dt(dt):
    dt_updated = datetime.strptime(dt,"%Y%m%d%H%M%S").strftime("%b %d %Y %H:%M")
    return dt_updated