package com.example.digitalinclusionapp.model

data class RegisterRequest(
    val username: String,
    val email: String,
    val password: String
)

data class TokenResponse(
    val access: String,
    val refresh: String
)