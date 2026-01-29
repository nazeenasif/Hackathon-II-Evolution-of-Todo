'use client';

import { Component } from 'react';

class GlobalErrorBoundary extends Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    // Update state so the next render will show the fallback UI.
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    // You can also log the error to an error reporting service
    console.error('Global error caught:', error, errorInfo);
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
  }

  render() {
    if (this.state.hasError) {
      // Safely convert error and errorInfo to strings
      const errorMessage = this.state.error ? JSON.stringify(this.state.error, Object.getOwnPropertyNames(this.state.error), 2) : 'Unknown error';
      const errorStack = this.state.error?.stack ? JSON.stringify(this.state.error.stack, null, 2) : '';
      const componentStack = this.state.errorInfo?.componentStack ? JSON.stringify(this.state.errorInfo.componentStack, null, 2) : '';

      // You can render any custom fallback UI
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-50">
          <div className="max-w-2xl w-full bg-white p-6 rounded-lg shadow-md">
            <h2 className="text-xl font-bold text-red-600 mb-4">Something went wrong</h2>
            <p className="text-gray-600 mb-4">An unexpected error occurred. Please try refreshing the page.</p>

            {/* Error details */}
            <details className="mb-4 bg-red-50 p-4 rounded border border-red-200">
              <summary className="font-medium text-red-700 cursor-pointer">Error Details</summary>
              <div className="mt-2 text-sm text-gray-700">
                <div className="font-semibold mb-1">Error Message:</div>
                <pre className="bg-gray-100 p-2 rounded overflow-auto text-xs whitespace-pre-wrap break-words">
                  {errorMessage}
                </pre>

                {errorStack && (
                  <>
                    <div className="font-semibold mt-2 mb-1">Error Stack:</div>
                    <pre className="bg-gray-100 p-2 rounded overflow-auto text-xs whitespace-pre-wrap break-words">
                      {errorStack}
                    </pre>
                  </>
                )}

                {componentStack && (
                  <>
                    <div className="font-semibold mt-2 mb-1">Component Stack:</div>
                    <pre className="bg-gray-100 p-2 rounded overflow-auto text-xs whitespace-pre-wrap break-words">
                      {componentStack}
                    </pre>
                  </>
                )}
              </div>
            </details>

            <button
              onClick={() => window.location.reload()}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium"
            >
              Refresh Page
            </button>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default GlobalErrorBoundary;