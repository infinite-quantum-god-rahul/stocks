import React from 'react';
import { StatusBar, Platform, View, Text, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { Provider } from 'react-redux';
import { PersistGate } from 'redux-persist/integration/react';
import FlashMessage from 'react-native-flash-message';
import Toast from 'react-native-toast-message';

// Store
import { store, persistor } from './store';

// Navigation
import AppNavigator from './navigation/AppNavigator';

// Services
import { ErrorBoundary } from './services/ErrorBoundary';

// Loading Component
const LoadingScreen = () => (
  <View style={styles.loadingContainer}>
    <Text style={styles.loadingText}>Loading JobMatchPro...</Text>
  </View>
);

const App: React.FC = () => {
  return (
    <ErrorBoundary>
      <Provider store={store}>
        <PersistGate loading={<LoadingScreen />} persistor={persistor}>
          <NavigationContainer>
            <StatusBar
              barStyle={Platform.OS === 'ios' ? 'dark-content' : 'light-content'}
              backgroundColor="#1a1a1a"
              translucent={false}
            />
            
            <AppNavigator />
            
            <FlashMessage position="top" />
            <Toast />
          </NavigationContainer>
        </PersistGate>
      </Provider>
    </ErrorBoundary>
  );
};

const styles = StyleSheet.create({
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#f5f5f5',
  },
  loadingText: {
    fontSize: 18,
    color: '#007AFF',
    fontWeight: '600',
  },
});

export default App;