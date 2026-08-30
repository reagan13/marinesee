import 'package:flutter/material.dart';

import 'screens/shell.dart';
import 'theme/tokens.dart';

class MarineSeeApp extends StatelessWidget {
  const MarineSeeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'MarineSee',
      debugShowCheckedModeBanner: false,
      theme: buildMarineSeeTheme(),
      home: const AppShell(),
    );
  }
}
