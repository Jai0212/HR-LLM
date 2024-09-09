<template>
    <div class="header-login">
        <h1>LLM for HR</h1>
    </div>

    <div class="login-container">
        <div class="form-group">
            <input v-model="email" type="email" placeholder="Email" class="input-field" />
        </div>
        <div class="form-group">
            <input v-model="password" type="password" placeholder="Password" class="input-field" />
        </div>
        <button @click="login" v-if="!loading" class="login-button">Login</button>
        <div class="signup-link">
            <p>Don't have an account? <a @click="goToSignUp">Sign Up</a></p>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import globalState from '../state/globalState';

export default {
    name: 'UserLogin',
    data() {
        return {
            email: '',
            password: '',
            loading: false,
            currEmail: localStorage.getItem('authToken') || globalState.currEmail,
        };
    },
    methods: {
        async login() {

            if (this.email == '' || this.password == '') {
                alert("Please fill in all fields");
                return;
            }

            try {
                const response = await axios.post(`${this.$BACKEND_URL}/login`, {
                    email: this.email,
                    password: this.password,
                });

                this.loading = true;

                if (response.data.success && response.data.details) {
                    this.$router.push('/home').catch(err => {
                        console.error("Navigation error login:", err);
                    });
                    globalState.currEmail = this.email;
                    this.currEmail = this.email;
                    localStorage.setItem('authToken', this.email);
                } else if (response.data.success) {
                    alert("Invalid email or password. Please try again.");
                }
                else {
                    alert("Error logging in. Please try again.");
                }

                this.loading = false;

            } catch (error) {
                console.error('Error logging in:', error);
                alert("Error logging in. Please try again.");
            }
        },
        goToSignUp() {
            this.$router.push('/signup');
        }
    }
}
</script>

<style scoped>
.login-container {
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

.login-button {
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

.login-button:hover {
    background-color: #2c6b2f;
}

.login-button:disabled {
    background-color: #c8e6c9;
    cursor: not-allowed;
}

.header-login {
    background-color: #4CAF50;
    border-radius: 10px;
    margin-bottom: 10px;
    border: 4px solid #196f1c;
    color: white;
    padding: 10px;
    align-items: center;
    padding: 15px 30px;
}

.signup-link {
    margin-top: 20px;
    font-size: 14px;
}

.signup-link a {
    color: #388e3c;
    cursor: pointer;
    text-decoration: underline;
}

.signup-link a:hover {
    color: #2c6b2f;
}
</style>
