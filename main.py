from datetime import datetime as dt
from datetime import timedelta


hora_atual = dt.now()


hora_final = hora_atual + timedelta(minutes=2)
print(hora_final.minute)
