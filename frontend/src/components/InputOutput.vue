<template>
  <div>
    <header class="header-home">
      <h1>LLM for HR - {{ companyName }}</h1>
      <div class="profile-container" @click="toggleDropdown">
        <img class="profile-icon" src="/profile_icon.png" alt="Profile Image">
        <transition name="fade">
          <div v-if="showDropdown" class="dropdown-menu">
            <button @click="logout">Logout</button>
          </div>
        </transition>
      </div>
    </header>

    <div class="parent-container">
      <textarea v-model="inputText" placeholder="Enter your query or request"></textarea>
      <button @click="getAnswer" v-if="!loading" class="generate-button">Generate Response</button>

      <transition name="fade">
        <div v-if="loading" class="loading">
          Loading...
        </div>
      </transition>

      <transition name="fade">
        <div v-if="outputText && !loading" class="output">
          <p>{{ outputText }}</p>
        </div>
      </transition>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import globalState from '../state/globalState';

export default {
  data() {
    return {
      inputText: '',
      outputText: '',
      showDropdown: false,
      loading: false,
      currEmail: localStorage.getItem('authToken') || globalState.currEmail,
      companyName: ''
    };
  },
  async mounted() {
    await this.getCompanyName();
  },
  methods: {
    async getAnswer() {
      this.loading = true;

      try {
        const response = await axios.post(`${this.$BACKEND_URL}/get-answer`, {
          context: '',
          question: this.inputText,
          email: this.currEmail,
        });
        this.outputText = response.data.answer;
      } catch (error) {
        console.error('Error fetching answer:', error);
        this.outputText = 'Error fetching answer. Please try again.';
      } finally {
        this.loading = false;
      }
    },

    async logout() {
      try {
        const response = await axios.post(`${this.$BACKEND_URL}/logout`, {});

        if (response.data.success) {
          this.$router.push('/').catch(err => {
            console.error("Navigation error home:", err);
          });

          globalState.currEmail = '';
          this.currEmail = '';
          localStorage.removeItem('authToken');
        }
        else {
          console.error('Error logging out');
        }
      } catch (error) {
        console.error('Error logging out:', error);
      }
    },

    async getCompanyName() {
      try {
        const response = await axios.post(`${this.$BACKEND_URL}/get-company`, { email: this.currEmail });
        this.companyName = response.data.companyName;
      } catch (error) {
        console.error('Error fetching company name:', error);
      }
    },

    toggleDropdown() {
      this.showDropdown = !this.showDropdown;
    }
  }
};
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
  background-color: #f0f4f8;
  margin: 0;
  padding: 0;
  color: #333;
}

header.header-home {
  background-color: #4CAF50;
  color: white;
  padding: 25px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 4px 8px rgba(36, 177, 57, 0.1);
  border-radius: 20px;
  border-bottom: 4px solid #388e3c;
  margin-bottom: 40px;
}

.header-home h1 {
  margin: 0;
  font-size: 1.5em;
}

.profile-container {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: relative;
}

.profile-icon {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  box-shadow: 0 10 20px rgba(0, 0, 0, 0.1);
}

.dropdown-menu {
  position: absolute;
  top: 50px;
  right: 0;
  background-color: white;
  border: 1px solid #ddd;
  border-radius: 5px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 6px;
  z-index: 1000;
}

.dropdown-menu button {
  background: none;
  border: none;
  padding: 10px;
  cursor: pointer;
  width: 100%;
  text-align: left;
  color: #333;
  transition: background-color 0.3s ease;
}

.dropdown-menu button:hover {
  background-color: #f0f0f0;
}

.parent-container {
  padding: 20px;
  max-width: 800px;
  margin: 20px auto;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

textarea {
  width: 96%;
  height: 150px;
  padding: 15px;
  margin-bottom: 20px;
  border: 1px solid #a5d6a7;
  border-radius: 5px;
  font-size: 16px;
  background-color: #f0f8f4;
  resize: none;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
}

.generate-button {
  display: block;
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  border-radius: 5px;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s ease;
}

.generate-button:hover {
  background-color: #388e3c;
}

.output {
  width: 96%;
  padding: 15px;
  border: 1px solid #a5d6a7;
  border-radius: 5px;
  background-color: #f9f9f9;
  margin-top: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.loading {
  position: fixed;
  top: 60%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  z-index: 1000;
  font-size: 16px;
  color: #4CAF50;
  text-align: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter,
.fade-leave-to

/* .fade-leave-active in <2.1.8 */
  {
  opacity: 0;
}
</style>
