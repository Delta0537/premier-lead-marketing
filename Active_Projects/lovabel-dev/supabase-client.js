// Supabase Client Configuration
import { createClient } from '@supabase/supabase-js'

// Get environment variables
const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL || 'https://kixghhmqnnnkhiuminoe.supabase.co'
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY || 'sb_publishable_4LFleAeJ2VAiRhK-iBtRlw_atTDx'

// Create Supabase client
export const supabase = createClient(supabaseUrl, supabaseAnonKey, {
  auth: {
    autoRefreshToken: true,
    persistSession: true,
    detectSessionInUrl: true
  }
})

// Helper functions for common operations
export const auth = {
  // Sign up new user
  signUp: async (email, password, metadata = {}) => {
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        data: metadata
      }
    })
    return { data, error }
  },

  // Sign in user
  signIn: async (email, password) => {
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    })
    return { data, error }
  },

  // Sign out user
  signOut: async () => {
    const { error } = await supabase.auth.signOut()
    return { error }
  },

  // Get current user
  getUser: async () => {
    const { data: { user }, error } = await supabase.auth.getUser()
    return { user, error }
  },

  // Listen to auth state changes
  onAuthStateChange: (callback) => {
    return supabase.auth.onAuthStateChange(callback)
  }
}

// Database helpers
export const db = {
  // Generic select
  select: (table, columns = '*') => supabase.from(table).select(columns),
  
  // Generic insert
  insert: (table, data) => supabase.from(table).insert(data),
  
  // Generic update
  update: (table, data) => supabase.from(table).update(data),
  
  // Generic delete
  delete: (table) => supabase.from(table).delete()
}

// Storage helpers
export const storage = {
  // Upload file
  upload: async (bucket, path, file) => {
    const { data, error } = await supabase.storage
      .from(bucket)
      .upload(path, file)
    return { data, error }
  },

  // Download file
  download: async (bucket, path) => {
    const { data, error } = await supabase.storage
      .from(bucket)
      .download(path)
    return { data, error }
  },

  // Get public URL
  getPublicUrl: (bucket, path) => {
    const { data } = supabase.storage
      .from(bucket)
      .getPublicUrl(path)
    return data.publicUrl
  }
}

export default supabase