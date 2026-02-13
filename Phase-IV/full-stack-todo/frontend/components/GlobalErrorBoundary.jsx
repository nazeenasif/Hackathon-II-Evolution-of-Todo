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
        <div className="min-h-screen flex items-center justify-center bg-background relative overflow-hidden">
          {/* Background decoration */}
          <div className="absolute inset-0 -z-10 overflow-hidden">
            <div className="absolute -top-40 -right-40 w-80 h-80 bg-destructive/10 rounded-full blur-3xl"></div>
            <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-destructive/5 rounded-full blur-3xl"></div>
          </div>

          <div className="max-w-2xl w-full bg-card/90 backdrop-blur-sm p-6 rounded-xl shadow-xl border border-border/50">
            <div className="text-center mb-6">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-destructive/10 mb-4">
                <span className="text-3xl">❌</span>
              </div>
              <h2 className="text-xl font-bold text-foreground mb-2">Something went wrong</h2>
              <p className="text-muted-foreground">An unexpected error occurred. Please try refreshing the page.</p>
            </div>

            {/* Error details */}
            <details className="mb-6 bg-destructive/5 border border-destructive/20 p-4 rounded-xl backdrop-blur-sm">
              <summary className="font-medium text-destructive cursor-pointer flex items-center space-x-2">
                <span>Error Details</span>
                <span>▼</span>
              </summary>
              <div className="mt-3 text-sm text-muted-foreground">
                <div className="font-semibold mb-2 text-foreground">Error Message:</div>
                <pre className="bg-background/50 p-3 rounded-lg overflow-auto text-xs whitespace-pre-wrap break-words border border-border/30">
                  {errorMessage}
                </pre>

                {errorStack && (
                  <>
                    <div className="font-semibold mt-3 mb-2 text-foreground">Error Stack:</div>
                    <pre className="bg-background/50 p-3 rounded-lg overflow-auto text-xs whitespace-pre-wrap break-words border border-border/30">
                      {errorStack}
                    </pre>
                  </>
                )}

                {componentStack && (
                  <>
                    <div className="font-semibold mt-3 mb-2 text-foreground">Component Stack:</div>
                    <pre className="bg-background/50 p-3 rounded-lg overflow-auto text-xs whitespace-pre-wrap break-words border border-border/30">
                      {componentStack}
                    </pre>
                  </>
                )}
              </div>
            </details>

            <div className="flex justify-center">
              <button
                onClick={() => window.location.reload()}
                className="bg-gradient-to-r from-destructive to-destructive/90 hover:from-destructive/90 hover:to-destructive/80 text-destructive-foreground px-6 py-3 rounded-xl font-medium shadow-lg hover:shadow-xl transition-all duration-200 hover:scale-105 active:scale-95"
              >
                Refresh Page
              </button>
            </div>
          </div>
        </div>
      );
    }

    return this.props.children;
  }
}

export default GlobalErrorBoundary;