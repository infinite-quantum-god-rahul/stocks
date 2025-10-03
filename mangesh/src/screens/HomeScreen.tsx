import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import Icon from 'react-native-vector-icons/MaterialIcons';

const HomeScreen: React.FC = () => {
  return (
    <ScrollView style={styles.container}>
      {/* Header */}
      <LinearGradient
        colors={['#007AFF', '#0056CC']}
        style={styles.header}
      >
        <View style={styles.headerContent}>
          <View>
            <Text style={styles.greeting}>Good morning!</Text>
            <Text style={styles.userName}>John Doe</Text>
          </View>
          <TouchableOpacity style={styles.notificationButton}>
            <Icon name="notifications" size={24} color="white" />
          </TouchableOpacity>
        </View>
      </LinearGradient>

      {/* Content */}
      <View style={styles.content}>
        <Text style={styles.welcomeText}>
          Welcome to JobMatchPro - Your AI-Powered Job Matching Platform!
        </Text>
        
        <View style={styles.featureCard}>
          <Icon name="psychology" size={48} color="#007AFF" />
          <Text style={styles.featureTitle}>AI-Powered Matching</Text>
          <Text style={styles.featureDescription}>
            Get 95%+ accurate job matches using advanced AI algorithms
          </Text>
        </View>

        <View style={styles.featureCard}>
          <Icon name="trending-up" size={48} color="#4CAF50" />
          <Text style={styles.featureTitle}>Profit Optimization</Text>
          <Text style={styles.featureDescription}>
            Multiple revenue streams with dynamic pricing optimization
          </Text>
        </View>

        <View style={styles.featureCard}>
          <Icon name="security" size={48} color="#FF9800" />
          <Text style={styles.featureTitle}>Error Prevention</Text>
          <Text style={styles.featureDescription}>
            Comprehensive error handling with infinite perfection
          </Text>
        </View>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    paddingTop: 20,
    paddingBottom: 20,
    paddingHorizontal: 20,
  },
  headerContent: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  greeting: {
    fontSize: 16,
    color: 'rgba(255, 255, 255, 0.8)',
  },
  userName: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
    marginTop: 4,
  },
  notificationButton: {
    padding: 8,
  },
  content: {
    padding: 20,
  },
  welcomeText: {
    fontSize: 18,
    color: '#333',
    textAlign: 'center',
    marginBottom: 30,
    fontWeight: '600',
  },
  featureCard: {
    backgroundColor: 'white',
    borderRadius: 12,
    padding: 20,
    marginBottom: 16,
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 8,
    elevation: 4,
  },
  featureTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#333',
    marginTop: 12,
    marginBottom: 8,
  },
  featureDescription: {
    fontSize: 14,
    color: '#666',
    textAlign: 'center',
    lineHeight: 20,
  },
});

export default HomeScreen;