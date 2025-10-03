import { Job } from '../services/JobMatchingService';

export type RootStackParamList = {
  MainTabs: undefined;
  JobDetails: { job: Job };
  Chat: { companyName: string; jobId: string };
  Premium: undefined;
  Analytics: undefined;
};

export type TabParamList = {
  Home: undefined;
  Matches: undefined;
  Profile: undefined;
  Settings: undefined;
};

export type AppState = {
  isInitialized: boolean;
  isAuthenticated: boolean;
  currentUser: User | null;
  networkStatus: 'online' | 'offline';
  theme: 'light' | 'dark';
};

export interface User {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  isPremium: boolean;
  subscriptionPlan: string;
  tier: string;
  preferences: UserPreferences;
  stats: UserStats;
}

export interface UserPreferences {
  notifications: {
    email: boolean;
    push: boolean;
    sms: boolean;
  };
  privacy: {
    profileVisibility: 'public' | 'private' | 'connections';
    showSalary: boolean;
    showContactInfo: boolean;
  };
  jobAlerts: {
    frequency: 'daily' | 'weekly' | 'monthly';
    types: string[];
    locations: string[];
  };
}

export interface UserStats {
  totalApplications: number;
  totalMatches: number;
  responseRate: number;
  averageMatchScore: number;
  profileCompleteness: number;
  lastActive: string;
}



