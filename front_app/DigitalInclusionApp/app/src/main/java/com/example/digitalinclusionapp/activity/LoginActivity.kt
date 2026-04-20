package com.example.digitalinclusionapp.activity

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.lifecycle.ViewModelProvider
import com.example.digitalinclusionapp.R
import com.example.digitalinclusionapp.api.RetrofitInstance
import com.example.digitalinclusionapp.repository.AuthRepository
import com.example.digitalinclusionapp.util.TokenManager
import com.example.digitalinclusionapp.viewmodel.*

class LoginActivity : AppCompatActivity() {
    private lateinit var viewModel: AuthViewModel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        val tokenManager = TokenManager(this)
        val repository = AuthRepository(RetrofitInstance.api)
        val factory = AuthViewModelFactory(repository)
        viewModel = ViewModelProvider(this, factory).get(AuthViewModel::class.java)

        val btnLogin = findViewById<Button>(R.id.btnLogin)
        val etUser = findViewById<EditText>(R.id.etLoginUsername)
        val etPass = findViewById<EditText>(R.id.etLoginPassword)

        btnLogin.setOnClickListener {
            val user = etUser.text.toString()
            val pass = etPass.text.toString()
            if (user.isNotEmpty() && pass.isNotEmpty()) {
                viewModel.login(user, pass, tokenManager)
            }
        }

        viewModel.loginSuccess.observe(this) { success ->
            if (success) {
                startActivity(Intent(this, StoreActivity::class.java))
                finish()
            } else {
                Toast.makeText(this, "Ошибка входа", Toast.LENGTH_SHORT).show()
            }
        }
    }
}