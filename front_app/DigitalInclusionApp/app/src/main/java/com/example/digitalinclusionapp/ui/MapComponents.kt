package com.example.digitalinclusionapp.ui

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.example.digitalinclusionapp.model.PlaceInfo

@Composable
fun TopSearchBar(modifier: Modifier = Modifier) {
    Surface(
        modifier = modifier
            .fillMaxWidth()
            .padding(16.dp)
            .height(56.dp),
        shape = RoundedCornerShape(12.dp),
        color = Color.White,
        shadowElevation = 4.dp
    ) {
        Row(
            verticalAlignment = Alignment.CenterVertically,
            modifier = Modifier.padding(horizontal = 16.dp)
        ) {
            Icon(Icons.Default.Search, contentDescription = null, tint = Color.Gray)
            Text(
                "Поиск по адресу",
                modifier = Modifier
                    .weight(1f)
                    .padding(start = 12.dp),
                color = Color.Gray,
                fontSize = 14.sp
            )
            Icon(Icons.Default.Tune, contentDescription = "Filter", tint = Color.Gray)
        }
    }
}

// Renamed from InfoPopupCard to HospitalPopup to match your MainMapScreen import
@Composable
fun HospitalPopup(place: PlaceInfo, modifier: Modifier = Modifier) {
    Card(
        modifier = modifier.fillMaxWidth(0.9f),
        shape = RoundedCornerShape(16.dp),
        colors = CardDefaults.cardColors(containerColor = Color.White),
        elevation = CardDefaults.cardElevation(defaultElevation = 8.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            // Header
            Row {
                Icon(Icons.Default.LocationOn, "Loc", tint = Color(0xFF2196F3))
                Spacer(Modifier.width(8.dp))
                Column {
                    Text(place.name, fontWeight = FontWeight.Bold, fontSize = 16.sp)
                    Text(place.category, fontSize = 12.sp, color = Color.Gray)
                }
            }

            // Rating
            Row(
                verticalAlignment = Alignment.CenterVertically,
                modifier = Modifier.padding(top = 8.dp)
            ) {
                Text("${place.rating}", fontWeight = FontWeight.Bold, fontSize = 14.sp)
                Text(" ★★★★☆", color = Color(0xFFFFC107))
                Text(" (${place.reviewCount} отзывов)", fontSize = 12.sp, color = Color.Gray)
            }

            Spacer(Modifier.height(12.dp))

            // Details - Matching the field names in your PlaceInfo model
            DetailItem(Icons.Default.Place, place.address)
            DetailItem(Icons.Default.Phone, place.phone)

            // Combining Description and Status for the accessibility row
            DetailItem(
                Icons.Default.Accessible,
                "${place.accessibilityDescription} - ${place.accessibilityStatus}"
            )

            Spacer(Modifier.height(16.dp))

            // Action Button
            Button(
                onClick = { },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(44.dp),
                shape = RoundedCornerShape(8.dp),
                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF2196F3))
            ) {
                // Button is intentionally empty to match the screenshot UI
            }
        }
    }
}

@Composable
fun DetailItem(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String) {
    Row(
        modifier = Modifier.padding(vertical = 4.dp),
        verticalAlignment = Alignment.Top
    ) {
        Icon(
            icon,
            null,
            modifier = Modifier.size(16.dp),
            tint = Color(0xFF4CAF50) // Green color from original screenshot
        )
        Spacer(Modifier.width(8.dp))
        Text(text, fontSize = 12.sp, lineHeight = 16.sp)
    }
}