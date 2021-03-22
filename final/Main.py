import Kernel as K
import threading

st = threading.Thread(target=K.Kernel)
st.start()