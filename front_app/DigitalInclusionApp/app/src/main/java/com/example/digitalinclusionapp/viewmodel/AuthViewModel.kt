package com.example.digitalinclusionapp.viewmodel

import androidx.lifecycle.*
import com.example.digitalinclusionapp.model.*
import com.example.digitalinclusionapp.repository.AuthRepository
import com.example.digitalinclusionapp.util.TokenManager
import kotlinx.coroutines.launch

class AuthViewModel(private val repository: AuthRepository) : ViewModel() {
    val loginSuccess = MutableLiveData<Boolean>()
    val registerSuccess = MutableLiveData<Boolean>()
    val errorMessage = MutableLiveData<String>()

    fun login(username: String, pass: String, tokenManager: TokenManager) {
        viewModelScope.launch {
            try {
                val response = repository.login(mapOf("username" to username, "password" to pass))
                if (response.isSuccessful && response.body() != null) {
                    tokenManager.saveToken(response.body()!!.access)
                    loginSuccess.postValue(true)
                } else {
                    errorMessage.postValue("Неверный логин или пароль")
                }
            } catch (e: Exception) {
                errorMessage.postValue("Нет связи с сервером")
            }
        }
    }

    fun register(request: RegisterRequest) {
        viewModelScope.launch {
            try {
                val response = repository.register(request)
                registerSuccess.postValue(response.isSuccessful)
            } catch (e: Exception) {
                errorMessage.postValue("Ошибка сети")
            }
        }
    }
}

class AuthViewModelFactory(private val repository: AuthRepository) : ViewModelProvider.Factory {
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        return AuthViewModel(repository) as T
    }
}