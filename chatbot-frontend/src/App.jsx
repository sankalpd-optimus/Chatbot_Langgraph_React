// App.jsx
import ChatBot from './Components/ChatBot';
import ErrorBoundary from './ErrorBoundary';

function App() {
  return (
    <div className="App">
      <h1>Chatbot</h1>
    <ErrorBoundary>
      <ChatBot />
    </ErrorBoundary> 
    </div>
  );
}

export default App;
