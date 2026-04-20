package com.example.digitalinclusionapp.activity

import android.os.Bundle
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import com.example.digitalinclusionapp.databinding.ActivitySignupBinding

class SignupActivity : AppCompatActivity() {
    private lateinit var binding: ActivitySignupBinding

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivitySignupBinding.inflate(layoutInflater)
        setContentView(binding.root)

        binding.btnRegister.setOnClickListener {
            val user = binding.etUsername.text.toString()
            if (user.isNotEmpty()) {
                Toast.makeText(this, "Привет, $user! Скоро добавим API", Toast.LENGTH_SHORT).show()
            }
        }
    }
}