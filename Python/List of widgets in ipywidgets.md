
Here’s a **hands-on “cheat sheet”** / quick reference for using **ipywidgets** in Jupyter notebooks — covering common widget types, how to display them, layout options, and basic interaction patterns.

---
## 🧰 **ipywidgets Cheat Sheet**

### 📌 **Import Essentials**

```python
import ipywidgets as widgets
from IPython.display import display
```

Widgets are interactive Python objects that appear in the notebook’s output area and sync with Python state. ([Jupyter Widgets](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Basics.html?utm_source=chatgpt.com "Simple Widget Introduction - IPyWidgets - Read the Docs"))

---
## 🔢 **Common Widget Types**

### **Numeric Widgets**

| Widget        | Description             | Example                                            |
| ------------- | ----------------------- | -------------------------------------------------- |
| `IntSlider`   | Slider for integers     | `widgets.IntSlider(value=5, min=0, max=10)`        |
| `FloatSlider` | Slider for floats       | `widgets.FloatSlider(value=0.5, min=0.0, max=1.0)` |
| `IntText`     | Text input for integers | `widgets.IntText(value=10)`                        |
| `FloatText`   | Text input for floats   | `widgets.FloatText(value=3.14)`                    |
| `IntProgress` | Progress bar            | `widgets.IntProgress(value=20, min=0, max=100)`    |

---
## 🔤 **Text & Display Widgets**

|Widget|Description|
|---|---|
|`Text`|Single-line text input|
|`Textarea`|Multi-line text|
|`Label`|Read-only label|
|`HTML`|Render HTML content|

```python
text = widgets.Text(description='Your name:')
display(text)
```

---
## 🔘 **Boolean & Toggle**

|Widget|Description|
|---|---|
|`Checkbox`|True / False toggle|
|`ToggleButton`|Button states on/off|
|`RadioButtons`|Select one option|
|`ToggleButtons`|Button group|

```python
checkbox = widgets.Checkbox(value=True, description='Enable')
display(checkbox)
```

---
## 🗂️ **Selection Widgets**

|Widget|Description|
|---|---|
|`Dropdown`|Choose one value from list|
|`SelectMultiple`|Choose multiple values|
|`Select`|Simple list selector|
|`Combobox`|Autocomplete picker|

```python
dd = widgets.Dropdown(options=['Red','Green','Blue'], description='Color')
display(dd)
```

---
## 📅 **Other Useful Widgets**

|Widget|Description|
|---|---|
|`DatePicker`|Choose a date|
|`ColorPicker`|Select color|
|`FileUpload`|Upload files|
|`Play`|Play control for animations|

---
## 🧱 **Layout & Styling**

You can control widget appearance with layout attributes:

```python
btn = widgets.Button(description='Click me',
                     layout=widgets.Layout(width='50%', height='40px'))
display(btn)
```

Layout supports CSS-like properties: `width`, `height`, `margin`, `padding`, `display`, `flex`, `grid`, etc. ([Jupyter Widgets](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Layout.html?utm_source=chatgpt.com "Layout of Jupyter widgets - IPyWidgets"))

---
## 🔄 **Displaying Widgets**

Widgets display automatically if returned from a cell or explicitly shown:

```python
slider = widgets.IntSlider()
display(slider)
```

Multiple display() calls on the same widget stay in sync. ([Jupyter Widgets](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Basics.html?utm_source=chatgpt.com "Simple Widget Introduction - IPyWidgets - Read the Docs"))

---
## 💡 **Connecting Widgets to Code**

### **Using `observe()`**

React to changes:

```python
def on_change(change):
    print("New value:", change['new'])

slider.observe(on_change, names='value')
display(slider)
```

This listens to widget trait changes. Change handlers get a dictionary with keys like `'new'` and `'old'`. ([Stack Overflow](https://stackoverflow.com/questions/34020789/ipywidgets-dropdown-widgets-what-is-the-onchange-event?utm_source=chatgpt.com "ipywidgets dropdown widgets: what is the onchange event?"))

---
### **Using `@interact` / `@interact_manual`**

Quickest way to link UI controls to a function:

```python
from ipywidgets import interact

@interact(x=(0,10))
def f(x=5):
    print(x)
```

It auto-creates a slider or dropdown based on function signature. ([IPython Cookbook](https://ipython-books.github.io/33-mastering-widgets-in-the-jupyter-notebook/?utm_source=chatgpt.com "3.3. Mastering widgets in the Jupyter Notebook"))

---

## 📦 **Widget Containers**

Useful for grouping multiple widgets:

```python
hb = widgets.HBox([slider, dd])
vb = widgets.VBox([text, hb])
display(vb)
```

This arranges widgets horizontally or vertically.

---

## 📜 **Widget Properties**

Common properties most widgets share:

- `value`: current value
- `description`: label text
- `disabled`: enable/disable
- `layout`: layout object
- `style`: style settings

You can inspect available trait keys with:

```python
widget.keys
```

([Jupyter Widgets](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20Basics.html?utm_source=chatgpt.com "Simple Widget Introduction - IPyWidgets - Read the Docs"))

---

## 📚 **Complete Reference**

For a full list of widgets and detailed docs, see the official list of core widgets and guides in the ipywidgets docs. ([Jupyter Widgets](https://ipywidgets.readthedocs.io/en/latest/examples/Widget%20List.html?utm_source=chatgpt.com "Widget List — Jupyter Widgets 8.1.7 documentation - IPyWidgets"))

---

If you want, I can also provide this in **printable PDF form** or a **Markdown file** to save as your own reference!