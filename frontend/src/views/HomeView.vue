<template>
  <div class="bg-dark text-white">
    <!-- Navigation Header -->
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top neon-navbar">
      <div class="container">
        <router-link class="navbar-brand d-flex align-items-center text-decoration-none" to="/">
          <span class="brand-circle d-flex align-items-center justify-content-center me-2 fw-bold fs-4">P</span>
          Vehicle Parking
        </router-link>

        <div class="navbar-nav ms-auto">
          <router-link class="nav-link fw-semibold" to="/login">
            <i class="fas fa-sign-in-alt me-1"></i> Login
          </router-link>
          <router-link class="nav-link fw-semibold" to="/register">
            <i class="fas fa-user-plus me-1"></i> Register
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section d-flex align-items-center">
      <div class="container text-center">
        <h1 class="hero-title gradient-text mb-4">
          Park Smarter, Not Harder!
        </h1>
        <p class="fs-5 text-light mb-3 hero-subtitle">
          Experience the future of parking with our intelligent management system designed for convenience and efficiency.
        </p>
        <p class="fs-6 text-muted mb-4 hero-subtext">
          Sign up today to enjoy real-time availability, seamless access, and detailed parking analytics at your fingertips.
        </p>
        <div class="d-flex gap-3 justify-content-center flex-wrap">
          <router-link to="/register" class="btn btn-primary btn-lg px-4 glowing-btn">
            Get Started
          </router-link>
          <router-link to="/login" class="btn btn-outline-primary btn-lg px-4 glowing-btn-outline">
            Login
          </router-link>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="py-5">
      <div class="container">
        <div class="row g-4">
          <!-- Card 1 -->
          <div class="col-lg-4 col-md-6">
            <div class="neon-card">
              <div class="neon-icon bg-primary-glow">
                <i class="fas fa-chart-line fs-2"></i>
              </div>
              <h5 class="fw-bold neon-card-title">Real-Time Monitoring</h5>
              <p class="neon-card-text">
                Instantly track parking availability with live updates and notifications for smooth operations.
              </p>
            </div>
          </div>
          <!-- Card 2 -->
          <div class="col-lg-4 col-md-6">
            <div class="neon-card">
              <div class="neon-icon bg-success-glow">
                <i class="fas fa-chart-bar fs-2"></i>
              </div>
              <h5 class="fw-bold neon-card-title">Smart Analytics</h5>
              <p class="neon-card-text">
                Understand peak hours, usage patterns, and optimize revenue with actionable insights.
              </p>
            </div>
          </div>
          <!-- Card 3 -->
          <div class="col-lg-4 col-md-6">
            <div class="neon-card">
              <div class="neon-icon bg-info-glow">
                <i class="fas fa-mobile-alt fs-2"></i>
              </div>
              <h5 class="fw-bold neon-card-title">Multi-Device Access</h5>
              <p class="neon-card-text">
                Manage your parking system from any device with our responsive web platform and mobile app.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats Section -->
    <section class="py-5 bg-gradient-stats">
      <div class="container">
        <div class="row g-4 text-center">
          <div class="col-lg-3 col-md-6">
            <div class="h2 neon-text">10,000+</div>
            <p class="text-light mb-0">Parking Spots Managed</p>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="h2 neon-text">500+</div>
            <p class="text-light mb-0">Active Locations</p>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="h2 neon-text">99.9%</div>
            <p class="text-light mb-0">System Uptime</p>
          </div>
          <div class="col-lg-3 col-md-6">
            <div class="h2 neon-text">24/7</div>
            <p class="text-light mb-0">Customer Support</p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="py-5 text-center">
      <div class="container">
        <h2 class="display-5 fw-bold gradient-text mb-3">Ready to Transform Your Parking Operations?</h2>
        <p class="fs-5 mb-4 opacity-75 text-light">
          Join hundreds of businesses that trust Vehicle Parking for their parking management needs.
        </p>
        <router-link to="/register" class="btn btn-primary btn-lg px-5 glowing-btn">
          Start Free Trial
        </router-link>
      </div>
    </section>

    <!-- Footer -->
    <footer class="py-4 text-center neon-footer">
      <div class="container">
        <p class="mb-0">&copy; 2025 Vehicle Parking | All rights reserved</p>
      </div>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'HomeView'
}
</script>

<style scoped>
/* ===================== General Gradient Text ===================== */
.gradient-text {
  background: linear-gradient(90deg, #007bff, #00eaff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

/* ===================== Navbar ===================== */
.neon-navbar {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(15px);
  box-shadow: 0 0 20px rgba(0, 123, 255, 0.3);
}

.brand-circle {
  background: #fff;
  color: #007bff;
  border-radius: 50%;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
}

/* ===================== Hero Section ===================== */
.hero-section {
  min-height: 80vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: radial-gradient(circle at top left, #001f44, #001022);
}

.hero-title {
  font-size: 3rem;
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.7);
}

.hero-subtitle {
  animation: fadeInUp 1s ease forwards;
}

.hero-subtext {
  animation: fadeInUp 1.2s ease forwards;
}

/* ===================== Buttons ===================== */
.glowing-btn {
  border-radius: 14px;
  transition: all 0.3s ease;
  box-shadow: 0 0 15px rgba(0, 123, 255, 0.7);
}

.glowing-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 30px rgba(0, 255, 255, 1);
}

.glowing-btn-outline {
  border-radius: 14px;
  transition: all 0.3s ease;
  box-shadow: 0 0 10px rgba(0, 123, 255, 0.5);
  border: 1px solid rgba(0, 123, 255, 0.5);
}

.glowing-btn-outline:hover {
  transform: translateY(-3px);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.8);
  background: rgba(0, 123, 255, 0.1);
}

/* ===================== Neon Cards ===================== */
.neon-card {
  background: linear-gradient(145deg, rgba(0,123,255,0.1), rgba(0,255,255,0.1));
  border-radius: 20px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.4s ease;
  border: 2px solid rgba(0, 123, 255, 0.3);
  backdrop-filter: blur(12px);
  box-shadow: 0 0 20px rgba(0, 123, 255, 0.2), 0 0 40px rgba(0, 123, 255, 0.1) inset;
}

.neon-card:hover {
  transform: translateY(-10px) scale(1.05);
  border-color: rgba(0, 255, 255, 0.8);
  box-shadow: 0 0 40px rgba(0, 255, 255, 0.7), 0 0 60px rgba(0, 123, 255, 0.4) inset;
}

.neon-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 15px auto;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.neon-card:hover .neon-icon {
  transform: rotate(10deg) scale(1.2);
  box-shadow: 0 0 20px rgba(0, 255, 255, 0.7);
}

.neon-card-title {
  color: #00eaff;
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.7);
  margin-bottom: 0.8rem;
}

.neon-card-text {
  color: rgba(255, 255, 255, 0.85);
  font-size: 0.95rem;
  line-height: 1.5;
}

/* ===================== Stats ===================== */
.bg-gradient-stats {
  background: linear-gradient(90deg, #001f44, #001022);
  padding: 4rem 0;
}

.neon-text {
  text-shadow: 0 0 15px rgba(0, 255, 255, 0.8);
  transition: transform 0.3s ease;
}

.neon-text:hover {
  transform: scale(1.1);
}

/* ===================== Footer ===================== */
.neon-footer {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(12px);
  box-shadow: 0 -5px 25px rgba(0, 123, 255, 0.2);
}

/* ===================== Animations ===================== */
@keyframes fadeInUp {
  0% { opacity: 0; transform: translateY(20px); }
  100% { opacity: 1; transform: translateY(0); }
}
</style>
