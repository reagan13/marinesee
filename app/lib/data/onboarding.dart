import 'package:flutter/material.dart';

class OnboardingSlide {
  const OnboardingSlide({
    required this.icon,
    required this.title,
    required this.body,
    required this.imageAsset,
  });

  final IconData icon;
  final String title;
  final String body;
  final String imageAsset;
}

// Hero photos sourced from Unsplash (license: unsplash.com/license).
const onboardingSlides = [
  OnboardingSlide(
    icon: Icons.photo_camera_outlined,
    title: 'Identify seagrass',
    body:
        'Take a photo or pick one from the gallery. Identification uses an SVM.',
    imageAsset: 'assets/images/onboarding/identify.jpg',
  ),
  OnboardingSlide(
    icon: Icons.menu_book_outlined,
    title: 'Browse the library',
    body:
        'Nine documented seagrass species from Mati City, Davao Oriental.',
    imageAsset: 'assets/images/onboarding/library.jpg',
  ),
  OnboardingSlide(
    icon: Icons.waves_outlined,
    title: 'Learn as you go',
    body:
        'Open a species profile for the study fields, then the growth clip when a file is ready.',
    imageAsset: 'assets/images/onboarding/learn.png',
  ),
];
