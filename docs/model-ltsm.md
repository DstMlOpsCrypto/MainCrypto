# LTSM

## What is LSTM

LSTM is a type of _Recurrent Neural Network (RNN)_ designed to handle sequential data. Unlike traditional neural networks, LSTMs have a special architecture that allows them to remember information for long periods, making them particularly useful for tasks like time series forecasting, speech recognition, and natural language processing.

## LSTM within the Machine Learning and Deep Learning Ecosystem

### Machine Learning Ecosystem

The machine learning ecosystem includes a variety of models and techniques for analyzing data and making predictions. Some key components include:

* **Supervised Learning**: Algorithms that learn from labeled data (e.g., Linear Regression, Decision Trees).

* **Unsupervised Learning**: Algorithms that find patterns in data without labeled responses (e.g., K-Means Clustering, PCA).

* **Reinforcement Learning**: Algorithms that learn by interacting with an environment and receiving feedback (e.g., Q-Learning).


### Deep Learning Ecosystem

Within the broader machine learning ecosystem, deep learning represents a subset that focuses on neural networks with multiple layers. 

Key components include:

* **Feedforward Neural Networks (FNNs)**: Basic neural networks where information moves in one direction, from input to output.

* **Convolutional Neural Networks (CNNs)**: Specialized for processing grid-like data, such as images.

* **Recurrent Neural Networks (RNNs)**: Designed for sequential data, such as time series or language.


### Position of LSTM within Deep Learning

Long Short-Term Memory (LSTM) networks are a type of _Recurrent Neural Network (RNN)_. They are designed to address the limitations of traditional RNNs, specifically their difficulty in learning long-term dependencies.

#### Characteristics of LSTM:

* **Memory Cells**: LSTMs have memory cells that can store information over long periods.

* **Gates**: They use gates (input, forget, and output gates) to control the flow of information.

#### Role in Time Series and Sequential Data:

LSTMs are particularly effective for tasks where the sequence of data points matters. Examples include:

* **Time Series Forecasting**: Predicting future values based on past observations.

* **Speech Recognition**: Understanding spoken language by analyzing sequential audio data.

* **Natural Language Processing (NLP)**: Tasks like text generation, translation, and sentiment analysis.


## How does LSTM work

Traditional RNNs face challenges with long-term dependencies because they suffer from the _vanishing gradient problem_. During training, the gradients (used to update the network weights) can become very small, effectively "forgetting" earlier data in the sequence. This limitation makes it hard for RNNs to learn dependencies that span over long sequences.

??? info "Go deeper"
    See more [A Beginner's Guide to LSTMs and Recurrent Neural Networks](https://wiki.pathmind.com/lstm)


### Problem with Traditional RNNs

Traditional RNNs face challenges with long-term dependencies because they suffer from the vanishing gradient problem. During training, the gradients (used to update the network weights) can become very small, effectively "forgetting" earlier data in the sequence. 

This limitation makes it hard for RNNs to learn dependencies that span over long sequences.

## LSTM Architecture

LSTMs address the limitations of traditional RNNs with a more complex architecture, featuring a set of gates that control the flow of information. 

LSTMs have a unique structure with gates that control the flow of information. These gates are:

### Cell State \( (C_t) \)

The cell state is the memory of the network. It carries information across different time steps, allowing the LSTM to remember important details over long sequences.

### Gates

LSTMs have three types of gates that regulate the cell state:

#### Forget Gate \( (C_t) \)

    * Decides what information to discard from the cell state.

#### Input Gate \( (i_t) \)

    * Determines which values from the input to update the cell state.

#### Output Gate \( (O_t) \)

    * Controls what part of the cell state to output.

### The Flow of Information in LSTM

#### Forget Gate

At each time step \( t \), the forget gate determines what fraction of the previous cell state (\( C_{t-1} \)) to forget based on the current input (\( x_t \)) and previous hidden state (\( h_{t-1} \)):

\[ f_t = \sigma(W_f \cdot [h_{t-1}, x_t] + b_f) \]

Where \( \sigma \) is the sigmoid function, and \( W_f \)  and \( b_f \) are the weights and biases of the forget gate.

=== "What does it mean ?"

    _\( f_t \) :_ This is the output of the forget gate at time step. It decides how much information from the previous cell state should be forgotten.

    _\( \sigma \) :_ This is the sigmoid activation function. It squashes its input to be between 0 and 1. Essentially, it acts like a gate that decides what fraction of the information to pass through.

    _\( W_f \) :_ These are the weights associated with the forget gate. They determine the importance of each input feature.

    _\( h_{t-1} \) :_ This is the hidden state from the previous time step. It contains information from the past time steps.

    _\( x_t \) :_ This is the input at the current time step. It contains the current data point or feature being processed.

    _\( b_f \) :_ This is the bias term associated with the forget gate. It helps to adjust the output of the gate.


=== "How It Works"

    _1. Inputs to the Forget Gate:_

    * The hidden state from the previous time step \( h_{t-1} \) and the current input \( x_t \) are combined. 
    * This combination is essentially a way to capture both past information and current information.

    _2. Weighted Sum:_

    * The combined input is then multiplied by the weight matrix \( W_f \), which helps to scale the input features based on their importance.

    _3. Adding Bias:_

    * The bias \( b_f \) is added to the result. 
    * The bias ensures that the gate can operate even when the input values are zero.

    _4. Sigmoid Activation:_

    * Finally, the sigmoid function \( \sigma \) is applied. 
    * The sigmoid function squashes the result to be between 0 and 1. 
    * This squashing is crucial because it tells the model how much of the previous cell state should be "forgotten." 
    * A value close to 0 means "forget everything," and a value close to 1 means "keep everything."

=== "In Simple Terms"

    * Imagine you are trying to remember something important for your tasks over a week. Each day (time step), you decide how much of the previous day's information to keep (hidden state) and how much of today's new information (current input) to consider. The forget gate helps you decide how much of the past information you should retain or discard, based on the relevance of the new information you are receiving.

    * The combination of past information and current input, adjusted by weights and biases, goes through a "decision function" (sigmoid) that outputs a value between 0 and 1. This value guides you on how much of the past information to keep and how much to forget.


=== "Why It Matters"

    * The forget gate is crucial because it helps the LSTM model manage long-term dependencies. 
    * By selectively forgetting irrelevant information, the model can focus on the more pertinent details, thereby improving its performance on tasks involving sequential data, like time series forecasting and language modeling.

#### Input Gate

The input gate decides what new information to add to the cell state. 
It consists of two parts:

##### The update candidate

\[ \tilde{C_t} = \tanh(W_C \cdot [h_{t-1}, x_t] + b_C) \]

##### The gate itself

\[ i_t = \sigma(W_i \cdot [h_{t-1}, x_t] + b_i) \]

#### Update Cell State

The new cell state is a combination of the old cell state (modified by the forget gate) and the new candidate (modulated by the input gate):

\[ C_t = f_t * C_{t-1} + i_t * \tilde{C_t} \]


=== "What does it mean ?"

    _\( \tilde C \):_ This is the new candidate value for the cell state. It represents potential new information that could be added to the cell state.

    _\( i_t \):_ This is the output of the input gate at time step \( t \). It decides how much of the new candidate value should be added to the cell state.

    _\( \tanh \):_ This is the hyperbolic tangent activation function. It squashes its input to be between -1 and 1, helping to ensure the values stay within a reasonable range.

    _\( \sigma \):_ This is the sigmoid activation function. It squashes its input to be between 0 and 1.

    _\( W_c \) and \( W_i \):_ These are the weights associated with the update candidate and input gate, respectively. They determine the importance of each input feature.

    _\( h_{t-1} \):_ This is the hidden state from the previous time step. It contains information from past time steps.

    _\( Xt \):_ This is the input at the current time step  \( t \). It contains the current data point or feature being processed.

    _\( b_c \) and \( b_i \):_ These are the biases associated with the update candidate and input gate, respectively. They help adjust the output.


=== "How It Works"

    _1. Update Candidate:_

        * The update candidate \( \tilde C \) is calculated by combining the hidden state from the previous time step \( h_{t-1} \) and the current input \( Xt \). 
        * This combination is multiplied by the weight matrix \( W_c \) and added to the bias \( b_c \). 
        * The result is then passed through the \( \tanh \) function to create the new candidate value (see formula).

    _2. Input Gate:_

        * The input gate \( i_t \) determines how much of the new candidate value should be added to the cell state. 
        * It combines the hidden state from the previous time step \( h_{t-1} \) and the current input \( Xt \), multiplies by the weight matrix \( W_i \), and adds the bias \( b_i \).
        * This result is passed through the \( \sigma \) function to output a value between 0 and 1, indicating the proportion of the candidate value to be added to the cell state (see formula).


=== "In Simple Terms"

    * Imagine you're trying to learn a new skill, like playing the piano. Every day, you practice (current input \( Xt \) ) and recall what you learned previously (hidden state \( h_{t-1} \) ). The input gate helps you decide how much of the new practice (update candidate \( \tilde C \) ) should be added to your overall skill level (cell state).

    _1. Update Candidate:_ Think of this as creating a draft of what new information (new practice) could potentially be added to your memory.

    _2. Input Gate:_ This acts like a filter, deciding how much of this new draft should actually be kept and added to your overall skill level.

=== "Why It Matters"

    * The input gate is crucial because it determines how much new information gets incorporated into the memory of the LSTM. By carefully regulating the flow of new information, the LSTM can effectively learn and adapt to complex patterns in sequential data.

    * This gating mechanism allows LSTMs to handle long-term dependencies better than traditional RNNs, making them more effective for tasks such as time series forecasting, language modeling, and speech recognition.

#### Output Gate

Finally, the output gate decides what to output based on the cell state and the input. The hidden state \( h_t \) is updated:

\[ o_t = \sigma(W_o \cdot [h_{t-1}, x_t] + b_o) \]

\[ h_t = o_t * \tanh(C_t) \]

=== "What does it mean ?"

    _\( Xt \):_ This is the output of the output gate at time step \( t \). It decides which parts of the cell state should be outputted.

    _\( h_t \):_ This is the hidden state at time step \( t \). It is the information that gets passed to the next time step and is used for making predictions or further processing.

    _\( \sigma \):_ This is the sigmoid activation function. It squashes its input to be between 0 and 1.

    _\( \tanh \):_ This is the hyperbolic tangent activation function. It squashes its input to be between -1 and 1.

    _\( W_0 \):_ These are the weights associated with the output gate. They determine the importance of each input feature.

    _\( h_{t-1} \):_ This is the hidden state from the previous time step. It contains information from past time steps.

    _\( W_t \):_ This is the input at the current time step \( t \). It contains the current data point or feature being processed.

    _\( b_0 \):_ This is the bias term associated with the output gate. It helps to adjust the output of the gate.

    _\( C_t \):_ This is the cell state at time step \( t \). It contains the memory of the network.

=== "How It Works"

    _1. Output Gate:_ 

        * The output gate \( O_t \) decides what part of the cell state should be outputted. It does this by combining the hidden state from the previous time step \( h_{t-1} \) and the current input \( X_t \). 
        * This combination is multiplied by the weight matrix \( W_O \) and added to the bias \( b_0 \).
        * The result is then passed through the sigmoid function \( \sigma \), which outputs a value between 0 and 1 (see formula).

    _2. Hidden State Update:_

        * The hidden state \( h_t \) is updated by taking the output of the output gate \( O_t \) and multiplying it element-wise with the hyperbolic tangent of the cell state \( C_t \)  (see formula).

=== "In Simple Terms"

    * Imagine you are working on a project, and each day you decide what information from your notes (cell state) you will use (output) for the next task (hidden state). 
    * The output gate helps you make this decision.

    -1. Output Gate:_

        * Think of this as a filter that decides which parts of your notes are relevant for the task at hand. It looks at what you learned previously (hidden state) and what you currently need (input).

    _2. Hidden State Update:_

        * Once the output gate has decided what to use, it combines this filtered information with the current state of your memory (cell state) to update your working notes (hidden state) for the next task.

=== "Why It Matters"

    * The output gate is crucial because it determines what information is passed on to the next time step and what is outputted by the LSTM. 
    * By controlling the flow of information, the output gate ensures that only the most relevant information is used for making predictions or further processing. 
    * This makes LSTMs effective for tasks like time series forecasting, language modeling, and speech recognition.
    * By filtering and updating the hidden state, LSTMs can maintain and utilize long-term dependencies in sequential data, which is essential for understanding complex patterns over time.


### Characteristics and Benefits

* **Long-Term Dependencies**: LSTMs can capture and utilize long-term dependencies in sequential data, thanks to their memory cells and gating mechanisms.

* **Versatility**: Suitable for various domains where sequential data is crucial, such as finance (time series forecasting), healthcare (patient monitoring), and NLP (language modeling).

* **Efficiency**: Although computationally intensive, LSTMs can learn complex patterns in data that other models might miss.

### Limitations

* **Complexity**: The architecture of LSTMs is more complex compared to traditional RNNs, requiring more computational resources.

* **Training Time**: LSTMs typically take longer to train due to their complexity and the need to backpropagate through time.

* **Sensitivity to Hyperparameters**: Performance can be significantly affected by the choice of hyperparameters, requiring careful tuning.