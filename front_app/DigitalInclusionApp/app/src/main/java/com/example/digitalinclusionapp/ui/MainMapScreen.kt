package com.example.digitalinclusionapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.material3.Scaffold
import androidx.compose.runtime.*
import androidx.compose.ui.Modifier
import androidx.compose.ui.Alignment
import androidx.compose.ui.unit.dp
import com.example.digitalinclusionapp.model.PlaceInfo
import com.google.maps.android.compose.*
import com.google.android.gms.maps.model.*

@Composable
fun MainMapScreen() {

    // 📍 Центр Алматы
    val startLocation = LatLng(43.238949, 76.889709)

    val cameraPositionState = rememberCameraPositionState {
        position = CameraPosition.fromLatLngZoom(startLocation, 13f)
    }

    // 🔥 MOCK DATA (временно вместо backend)
    val places = remember {
        listOf(
            PlaceInfo(
                name = "Городская больница №7",
                category = "Медицина",
                rating = 4.3f,
                reviewCount = 28,
                address = "Алматы, Калкаман",
                phone = "+7 777 111 11 11",
                accessibilityDescription = "Пандус, лифт",
                accessibilityStatus = "Частично доступен"
            ),
            PlaceInfo(
                name = "Аптека",
                category = "Медицина",
                rating = 4.0f,
                reviewCount = 12,
                address = "Алматы",
                phone = "+7 777 222 22 22",
                accessibilityDescription = "Без ступенек",
                accessibilityStatus = "Доступен"
            ),
            PlaceInfo(
                name = "Кафе",
                category = "Еда",
                rating = 4.5f,
                reviewCount = 45,
                address = "Алматы",
                phone = "+7 777 333 33 33",
                accessibilityDescription = "Узкий вход",
                accessibilityStatus = "Ограничен"
            )
        )
    }

    // 📍 координаты для мок-мест
    val coordinates = listOf(
        LatLng(43.2185, 76.7915),
        LatLng(43.2200, 76.8000),
        LatLng(43.2150, 76.7800)
    )

    Scaffold(
//        bottomBar = { AppBottomNavigation() }
    ){ padding ->

        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
        ) {

            GoogleMap(
                modifier = Modifier.fillMaxSize(),
                cameraPositionState = cameraPositionState
            ) {

                // 🔥 маркеры из mock данных
                places.forEachIndexed { index, place ->

                    Marker(
                        state = MarkerState(position = coordinates[index]),
                        title = place.name,
                        snippet = place.accessibilityStatus
                    )
                }
            }

            TopSearchBar(
                modifier = Modifier
                    .align(Alignment.TopCenter)
                    .padding(16.dp)
            )
        }
    }
}
