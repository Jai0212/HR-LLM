<template>
    <div class="header-signup">
        <h1>LLM for HR</h1>
    </div>

    <div class="signup-container">
        <div class="form-group">
            <input v-model="email" type="email" placeholder="Email" class="input-field" />
        </div>
        <div class="form-group">
            <input v-model="password" type="password" placeholder="Password" class="input-field" />
        </div>
        <div class="form-group">
            <input v-model="confirmPassword" type="password" placeholder="Confirm Password" class="input-field" />
        </div>
        <div class="form-group-dropdown">
            <select v-model="selectedCompany" class="select-field">
                <option value="" disabled selected>Select your company</option>
                <option v-for="company in companies" :key="company" :value="company">
                    {{ company }}
                </option>
            </select>
        </div>
        <button @click="signup" v-if="!loading" class="signup-button">Sign Up</button>
        <div class="login-link">
            <p>Already have an account? <a @click="goToLogin">Login</a></p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import globalState from '../state/globalState';

export default {
    name: 'UserSignUp',
    data() {
        return {
            email: '',
            password: '',
            confirmPassword: '',
            selectedCompany: '',
            loading: false,
            companies: ['Company A', 'Company B'],
            currEmail: localStorage.getItem('authToken') || globalState.currEmail,
        };
    },
    methods: {
        async signup() {

            if (this.email == '' || this.password == '' || this.confirmPassword == '' || this.selectedCompany == '') {
                alert("Please fill in all fields");
                return;
            }

            if (this.password !== this.confirmPassword) {
                alert("Passwords do not match");
                return;
            }

            try {
                const response = await axios.post(`${this.$BACKEND_URL}/signup`, {
                    email: this.email,
                    password: this.password,
                    company: this.selectedCompany
                });

                this.loading = true;
                
                if (response.data.success) {
                    this.$router.push('/home').catch(err => {
                    console.error("Navigation error signup:", err);
                });
                    globalState.currEmail = this.email;
                    this.currEmail = this.email;
                    localStorage.setItem('authToken', this.email);
                } else {
                    alert("Error signing up. Please try again.");
                }

                this.loading = false;

            } catch (error) {
                console.error('Error signing up:', error);
                alert("Error signing up. Please try again.");
            }
        },
        goToLogin() {
            this.$router.push('/');
        }
    }
}
</script>

<style scoped>
.signup-container {
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #fafafa;
    max-width: 450px;
    margin: auto;
    margin-top: 120px;
}

.form-group {
    margin-bottom: 15px;
    width: 100%;
}

.form-group-dropdown {
    margin-bottom: 15px;
    width: 106%;
}

.input-field {
    width: 93%;
    padding: 12px;
    border: 1px solid #a5d6a7;
    border-radius: 4px;
    font-size: 16px;
}

.input-field:focus {
    border-color: #81c784;
    outline: none;
    box-shadow: 0 0 4px rgba(129, 199, 132, 0.5);
}

.select-field {
    width: 93%;
    padding: 12px;
    border: 1px solid #a5d6a7;
    border-radius: 4px;
    font-size: 16px;
    background-color: #fff;
}

.select-field:focus {
    border-color: #81c784;
    outline: none;
    box-shadow: 0 0 4px rgba(129, 199, 132, 0.5);
}

.signup-button {
    width: 100%;
    padding: 12px;
    background-color: #388e3c;
    border: none;
    border-radius: 4px;
    color: #fff;
    font-size: 16px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.signup-button:hover {
    background-color: #2c6b2f;
}

.signup-button:disabled {
    background-color: #c8e6c9;
    cursor: not-allowed;
}

.header-signup {
    background-color: #4CAF50;
    border-radius: 10px;
    margin-bottom: 10px;
    border: 4px solid #196f1c;
    color: white;
    padding: 10px;
    align-items: center;
    padding: 15px 30px;
}

.login-link {
    margin-top: 20px;
    font-size: 14px;
}

.login-link a {
    color: #388e3c;
    cursor: pointer;
    text-decoration: underline;
}

.login-link a:hover {
    color: #2c6b2f;
}
</style>
