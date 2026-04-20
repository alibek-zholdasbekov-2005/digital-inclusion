package com.example.digitalinclusionapp.repository

import com.example.digitalinclusionapp.api.ApiService
import com.example.digitalinclusionapp.model.RegisterRequest

class AuthRepository(private val api: ApiService) {
    suspend fun register(user: RegisterRequest) = api.register(user)
    suspend fun login(credentials: Map<String, String>) = api.loginUser(credentials)
}