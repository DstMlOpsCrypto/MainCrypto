# Streamlit

This part presents an overview of Streamlit tool for educational purposes.

## Introduction to Streamlit

???- info "Link"

    * https://streamlit.io/
    * https://share.streamlit.io
    
Streamlit is—a framework for building interactive and shareable web applications for data science and machine learning projects in Python.created by Adrien Treuille, Thiago Teixeira, and Amanda Kelly.

## Main Characteristics of Streamlit

Streamlit simplify the creation of applications with just a few lines of Python code but allowing the creation of highly interactive applications with widgets like sliders, buttons, and file uploaders.

Streamlit automatically updates the app in real-time as code is edited and integrate well with popular visualization libraries such as Matplotlib, Plotly, and Altair.

Deploy Streamlit is easy the ease of deploying Streamlit apps using services like Streamlit Sharing or other cloud platforms.

### Key Points:

* Simple and easy to use
* Highly interactive with built-in widgets
* Real-time updates during development
* Integrates with popular visualization libraries
* Easy to deploy

## Architecture of Streamlit

### Components Overview

* **Scripts**: Explain that Streamlit apps are built using simple Python scripts.
* **Widgets**: Describe how widgets create interactivity within the app.
* **Data and State Management**: Discuss how Streamlit manages data and application state.
* **Streamlit Server**: Describe the role of the Streamlit server in running the application.

### Key Points:

* Python scripts form the backbone of Streamlit apps
* Widgets enable interactivity
* Streamlit handles data and state management seamlessly
* The server runs and serves the application

## Detailed Architectural Breakdown

### Scripts

A Streamlit script is essentially a Python script that leverages the Streamlit library to create interactive web applications for data science and machine learning projects. 
Here's a breakdown of the main components and structure of a typical Streamlit script

#### Importing Libraries

```python
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
```

Title and Header
```python
st.title("Bitcoin Price Prediction Dashboard")
st.header("Using LSTM Model")
```

Uploading and Displaying Data

```python
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.dataframe(data)
```

Data Visualization

```python
fig, ax = plt.subplots()
ax.plot(data['Date'], data['Close'])
st.pyplot(fig)
```


### Widgets

Streamlit widgets are interactive elements that allow users to input data and interact with your Streamlit application in real-time. These widgets enable the creation of dynamic and responsive web applications. 

The following snippets illustrate the way to implement widgets.

```python
import streamlit as st

st.title("Interactive Dashboard with Streamlit Widgets")

# Button
if st.button('Click Me'):
    st.write('Button clicked!')

# Checkbox
agree = st.checkbox('I agree')
if agree:
    st.write('Thanks for agreeing!')

# Radio Button
genre = st.radio('Choose a genre', ['Comedy', 'Drama', 'Documentary'])
st.write(f'You selected {genre}')

# Select Box
option = st.selectbox('Pick an option', ['Option 1', 'Option 2', 'Option 3'])
st.write(f'You selected {option}')

# Multi-Select
options = st.multiselect('Select options', ['Option 1', 'Option 2', 'Option 3'])
st.write('You selected:', options)

# Slider
age = st.slider('Select your age', 0, 100, 25)
st.write(f'Your age is {age}')

# Text Input
name = st.text_input('Enter your name')
st.write(f'Hello, {name}!')

# Text Area
feedback = st.text_area('Your feedback')
st.write('Thank you for your feedback!')

# Number Input
number = st.number_input('Enter a number', min_value=0, max_value=100, value=50)
st.write(f'You entered {number}')

# File Uploader
uploaded_file = st.file_uploader('Choose a file')
if uploaded_file is not None:
    st.write('File uploaded successfully')

# Date Input
date = st.date_input('Select a date')
st.write(f'You selected {date}')

# Color Picker
color = st.color_picker('Pick a color', '#00f900')
st.write(f'Selected color: {color}')

```

### Data and State Management

Discuss how Streamlit manages the state of the application using st.session_state for storing stateful information across reruns.

Explain the concept of lazy evaluation where Streamlit only re-executes parts of the script that are affected by changes.

Streamlit handles data and state management in a way that is both intuitive and effective for building interactive applications. Here’s a detailed explanation of how Streamlit manages data and state:

#### Stateless Execution Model

Streamlit operates on a stateless execution model, meaning that every time you interact with the app (e.g., by clicking a button, moving a slider), Streamlit re-runs the entire script from top to bottom. This ensures that the app remains in sync with the user's inputs.

However, this can create challenges when you need to maintain certain states across interactions, such as user selections or input data.

explain how streamlit management Data and State Management
Streamlit handles data and state management in a way that is both intuitive and effective for building interactive applications. Here’s a detailed explanation of how Streamlit manages data and state:

#### Stateless Execution Model

Streamlit operates on a stateless execution model, meaning that every time you interact with the app (e.g., by clicking a button, moving a slider), Streamlit re-runs the entire script from top to bottom. This ensures that the app remains in sync with the user's inputs.

However, this can create challenges when you need to maintain certain states across interactions, such as user selections or input data.

#### Widgets and Session State

Widgets as State Holders
Streamlit widgets not only provide interactivity but also serve as implicit state holders. When you use a widget like st.slider or st.text_input, Streamlit remembers the state of the widget (the current value) across reruns.

```python
age = st.slider('Select your age', 0, 100, 25)
st.write(f'Your age is {age}')
In this example, the selected age value is remembered each time the script reruns.
```
In this example, the selected age value is remembered each time the script reruns.

##### Session State
For more complex state management, Streamlit provides st.session_state, a dictionary-like object where you can store and retrieve stateful information across reruns. This allows for more advanced state management beyond what widgets offer.

```python
# Counter value is maintained and incremented across user interactions
if 'counter' not in st.session_state:
    st.session_state.counter = 0

if st.button('Increment'):
    st.session_state.counter += 1
st.write(f'Counter: {st.session_state.counter}')
```

In this example, the counter value is maintained and incremented across user interactions

#### Data Caching

To improve performance and avoid redundant computations, Streamlit offers caching through the @st.cache_data decorator. This allows expensive operations (e.g., data loading, heavy computations) to be executed once and reused in subsequent runs, significantly speeding up the app.

```python
@st.cache_data
def load_data():
    return pd.read_csv('large_dataset.csv')

data = load_data()
st.dataframe(data)
```

Here, load_data will only be executed once, and the result will be cached, making subsequent interactions much faster.

#### Managing Long-Running Tasks

For long-running tasks or processes, Streamlit provides various mechanisms such as:

* Progress Bars and Spinners: To provide visual feedback during long computations.
* Threads: To run background tasks without blocking the main app.

```python
import time

if st.button('Start Long Task'):
    with st.spinner('Processing...'):
        time.sleep(5)
    st.success('Task completed!')
```

This example shows how you can indicate to users that a task is running in the background.

#### Handling User Inputs and Interactions

Streamlit’s design ensures that user inputs and interactions are straightforward to handle. When a user interacts with a widget, Streamlit re-runs the script, allowing you to dynamically react to changes. 

This reactive programming model makes it easy to build complex, interactive applications without managing the control flow explicitly.

### Streamlit Server


The Streamlit server plays a crucial role in running and serving Streamlit applications.

#### Running a Streamlit App

When you run a Streamlit script using the command streamlit run your_script.py, several things happen:

* **Server Initialization**: The Streamlit CLI initializes the Streamlit server.

* **Script Execution**: The server executes the script from top to bottom.

* **Widget State Management**: The server keeps track of widget states (e.g., values of sliders, text inputs) to maintain consistency across interactions.

#### Architecture Overview

The Streamlit server architecture consists of the following key components:

* **Frontend**: The user interface of the Streamlit app, which is a web page rendered in a browser.
* **Backend**: The Python script that defines the app's behavior and logic, executed by the Streamlit server.
* **WebSocket Connection**: A WebSocket connection between the frontend and backend that facilitates real-time communication and updates.

#### Frontend-Backend Interaction

##### Initial Load

When you first open the Streamlit app in a web browser, the frontend sends a request to the Streamlit server.

The server responds by sending the initial rendering of the app, which includes the layout, widgets, and any static content.

##### User Interaction

When a user interacts with the app (e.g., moves a slider, clicks a button), the frontend sends this interaction data back to the server via the WebSocket connection.

The server re-executes the script from top to bottom, taking into account the new widget state, and sends the updated view back to the frontend.

This process ensures that the app remains interactive and responsive to user input in real-time.

#### Handling State and Data

* **Session State**: The server uses st.session_state to manage stateful information across script executions, ensuring that user inputs and other stateful data are preserved.

* **Caching**: Streamlit employs caching mechanisms (@st.cache_data) to store the results of expensive operations, improving performance by avoiding redundant computations.

#### Serving the App

The Streamlit server uses HTTP to serve the app to the user's browser.

The frontend is built using modern web technologies such as React, ensuring a responsive and interactive user experience.

#### Continuous Updates

The WebSocket connection allows for continuous updates between the frontend and backend.

Any changes in the script, such as modifications to data or layout, are immediately reflected in the browser, providing a seamless development experience.

#### Example Workflow

1. **Start the Server**: You run your Streamlit script using streamlit run app.py.

2. **Initial Execution**: The server executes the script, rendering the initial app state.

3. **User Interaction**: A user interacts with the app, such as moving a slider.

4. **Re-execution**: The server re-executes the script with the updated slider value.

5. **Update Frontend**: The updated app state is sent to the frontend, which re-renders the UI accordingly.

#### Benefits of the Streamlit Server Model

* **Real-time Interactivity**: The WebSocket connection ensures that any user interaction is immediately processed and reflected in the app.

* **Simplicity**: Developers can focus on writing Python code without worrying about the complexities of front-end development.

* **Performance**: Caching and efficient state management ensure that the app remains performant, even with complex data operations.

## Integration and Extensions

Streamlit is designed with flexibility and extensibility in mind, enabling seamless integration with other tools and libraries, as well as the creation of custom components to extend its functionality. 
Here’s an overview of Streamlit’s integration capabilities and extensions

### Integration with Data and Visualization Libraries

Streamlit integrates effortlessly with a wide range of data manipulation and visualization libraries, making it a powerful tool for data scientists and developers. Some commonly used libraries include:


#### Pandas: For data manipulation and analysis.

```python
import streamlit as st
import pandas as pd

df = pd.read_csv('data.csv')
st.dataframe(df)
```

#### NumPy: For numerical computations.

```python
import numpy as np

arr = np.random.randn(100)
```

#### Matplotlib: For creating static, animated, and interactive visualizations.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot([1, 2, 3, 4], [10, 20, 25, 30])
st.pyplot(fig)
```

#### Plotly: For interactive, web-based visualizations.

```python
import plotly.express as px

df = px.data.iris()
fig = px.scatter(df, x='sepal_width', y='sepal_length', color='species')
st.plotly_chart(fig)
```

#### Altair: For declarative statistical visualizations.

```python
import altair as alt

df = pd.DataFrame({
    'a': ['A', 'B', 'C', 'D', 'E'],
    'b': [5, 3, 6, 7, 2]
})
chart = alt.Chart(df).mark_bar().encode(
    x='a',
    y='b'
)
st.altair_chart(chart)
```

### Integration with Machine Learning Libraries

Streamlit supports integration with various machine learning libraries, enabling users to build and deploy machine learning models directly within their Streamlit apps.

#### scikit-learn: For implementing standard machine learning algorithms.

```python
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()
model.fit(X_train, y_train)
st.write(model.predict(X_test))
```

#### TensorFlow: For developing deep learning models.

```python
import tensorflow as tf

model = tf.keras.models.Sequential([
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
st.write(model.summary())
```


#### PyTorch: For creating flexible and dynamic deep learning models.

```python
import torch
import torch.nn as nn

class SimpleModel(nn.Module):
    def __init__(self):
        super(SimpleModel, self).__init__()
        self.fc1 = nn.Linear(10, 5)

    def forward(self, x):
        return self.fc1(x)

model = SimpleModel()
st.write(model)
```

### Custom Components

Streamlit’s custom components allow developers to create and integrate new functionalities that are not natively supported by Streamlit. This can be particularly useful for incorporating complex interactive elements or third-party widgets.


* **Streamlit Components**: Streamlit provides a components module that allows developers to create custom web components using HTML, CSS, and JavaScript. These components can then be embedded in Streamlit apps.

```python
import streamlit.components.v1 as components

# Create a simple HTML component
html_code = """
<div style='color: red;'>Hello, Streamlit!</div>
"""
components.html(html_code)
```

* **Streamlit Component Library**: A growing library of community-developed components that can be easily integrated into Streamlit apps.

### API Integration

Streamlit can also be used to call APIs and integrate external data sources, allowing dynamic data fetching and interaction.

```python
# Calling API
import requests

response = requests.get('https://api.example.com/data')
data = response.json()
st.write(data)
```

### Deployment Options

Streamlit offers several deployment options to share apps with others:

* Streamlit Sharing: A free hosting service provided by Streamlit for deploying Streamlit apps.
* Other Platforms: Streamlit apps can also be deployed on platforms like Heroku, AWS, GCP, and Azure.

## Benefits and Limitations

### Benefits

* Quick and easy to develop interactive apps
* Minimal learning curve for data scientists familiar with Python
* Real-time updates streamline the development process
* Broad integration with data and visualization libraries

### Limitations

* Primarily designed for simple to moderately complex applications
* Performance may degrade with very large datasets or highly complex visualizations
* Limited support for multi-page applications without additional libraries



## Conclusion

* Streamlit simplifies the creation of interactive data apps
* Its architecture supports rapid development and integration
* Ideal for data scientists and machine learning practitioners


## Streamlit in the project

Streamlit is our frontend application. It's the only service available only on the public network. It shares the public network with the gateway API which is used to access the private services securely. It's exposed on the port 8501.

### Structure

```
RepoCrypto/frontend/
├── Dockerfile              # Streamlit container configuration
├── app.py                  # Streamlit entry point
├── requirements.txt        # Python dependencies
├── utils/
│   ├── __init__.py
│   ├── api_client.py      # API client functions
│   └── auth.py            # authentification functions
└── pages/
    ├── __init__.py
    ├── account.py         # manage his account
    ├── administration.py  # manage user accounts
    ├── create_user.py     # create a new user
    ├── data_analysis.py   # data analysis of historical data
    ├── home.py            # home page
    ├── model.py           # model management
    └── predictions.py     # predictions visualization
```

Some pages are only accessible for admin users, such as administration.py and create_user. Other pages are accessible for all users. The frontend use the role and the token to manage the access to the pages.
The only service with which the frontend communicate is the gateway API. It's throught the API that the frontend can access authentification / authorization services and backend features.
In streamlit we used plotly to create the charts and display the data.