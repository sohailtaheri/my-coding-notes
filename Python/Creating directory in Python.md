Here are the common ways to **create a directory in Python** 📁🐍

---

### **✅ Modern & recommended (** **pathlib** )

```python
from pathlib import Path

Path("new_folder").mkdir()
```

Create parents if needed:

```python
Path("a/b/c").mkdir(parents=True, exist_ok=True)
```

---

### **✅ Classic ( os )


```python
import os

os.mkdir("new_folder")
```

With parents:

```python
os.makedirs("a/b/c", exist_ok=True)
```

---

### **✅ In Jupyter / terminal cell**

```python
!mkdir new_folder
```

Or recursively:

```python
!mkdir -p a/b/c
```

---

### **📝 Notes**

- exist_ok=True prevents errors if the folder already exists 👍
    
- pathlib is cleaner, safer, and more readable ✨
    
- All paths are relative to the **current working directory** (os.getcwd())
    

  

If you want to create folders **relative to the notebook location**, or based on a variable path, tell me and I’ll tailor it 🚀