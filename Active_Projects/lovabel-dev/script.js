// lovabel.dev — minimal vibe with Supabase integration

// Supabase Configuration for Delta0537 (cleanslate0537@gmail.com)
const SUPABASE_URL = 'https://kixghhmqnnnkhiuminoe.supabase.co' // Your lovabel-dev project
const SUPABASE_ANON_KEY = 'sb_publishable_4LFleAeJ2VAiRhK-iBtRlw_atTDx' // Your anon key

// Initialize Supabase client (you'll need to include the Supabase CDN in your HTML)
let supabase = null;

// Initialize Supabase when the CDN is loaded
function initSupabase() {
  if (typeof window.supabase !== 'undefined') {
    supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
    console.log('Supabase initialized');
  }
}

document.addEventListener('DOMContentLoaded', () => {
  const sections = document.querySelectorAll('.section');
  const navLinks = document.querySelectorAll('.nav a[href^="#"]');
  if (!sections.length || !navLinks.length) return;

  const onScroll = () => {
    const scrollY = window.scrollY;
    let currentId = null;
    sections.forEach((section) => {
      const id = section.getAttribute('id');
      const top = section.offsetTop - 100;
      const height = section.offsetHeight;
      if (id && scrollY >= top && scrollY < top + height) currentId = id;
    });
    navLinks.forEach((link) => {
      link.classList.toggle('active', link.getAttribute('href') === `#${currentId}`);
    });
  };

  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Initialize Supabase
  initSupabase();
});

// Supabase helper functions
const SupabaseHelpers = {
  // Authentication functions
  async signUp(email, password, userData = {}) {
    if (!supabase) return { error: 'Supabase not initialized' };
    
    const { data, error } = await supabase.auth.signUp({
      email,
      password,
      options: { data: userData }
    });
    
    if (error) console.error('Sign up error:', error);
    return { data, error };
  },

  async signIn(email, password) {
    if (!supabase) return { error: 'Supabase not initialized' };
    
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password
    });
    
    if (error) console.error('Sign in error:', error);
    return { data, error };
  },

  async signOut() {
    if (!supabase) return { error: 'Supabase not initialized' };
    
    const { error } = await supabase.auth.signOut();
    if (error) console.error('Sign out error:', error);
    return { error };
  },

  async getCurrentUser() {
    if (!supabase) return { user: null, error: 'Supabase not initialized' };
    
    const { data: { user }, error } = await supabase.auth.getUser();
    return { user, error };
  },

  // Database functions
  async insertData(table, data) {
    if (!supabase) return { error: 'Supabase not initialized' };
    
    const { data: result, error } = await supabase
      .from(table)
      .insert(data);
    
    if (error) console.error(`Insert error for ${table}:`, error);
    return { data: result, error };
  },

  async fetchData(table, columns = '*') {
    if (!supabase) return { error: 'Supabase not initialized' };
    
    const { data, error } = await supabase
      .from(table)
      .select(columns);
    
    if (error) console.error(`Fetch error for ${table}:`, error);
    return { data, error };
  },

  // Listen to auth state changes
  onAuthStateChange(callback) {
    if (!supabase) return null;
    return supabase.auth.onAuthStateChange(callback);
  }
};

// Make helpers available globally
window.SupabaseHelpers = SupabaseHelpers;
