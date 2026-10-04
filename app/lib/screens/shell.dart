import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../classify/api_classifier.dart';
import '../widgets/app_menu_sheet.dart';
import '../widgets/app_nav_bar.dart';
import '../widgets/aurora_atmosphere.dart';
import 'identify_screen.dart';
import 'library_screen.dart';

class AppShell extends StatefulWidget {
  const AppShell({super.key});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int _index = 0;
  final _classifier = ApiClassifier();
  final _identifyKey = GlobalKey<IdentifyScreenState>();

  @override
  Widget build(BuildContext context) {
    final pages = [
      IdentifyScreen(key: _identifyKey, classifier: _classifier),
      const LibraryScreen(),
    ];

    return Stack(
      fit: StackFit.expand,
      children: [
        const AuroraAtmosphere(),
        Scaffold(
          backgroundColor: Colors.transparent,
          extendBody: true,
          resizeToAvoidBottomInset: !kIsWeb,
          body: IndexedStack(index: _index, children: pages),
          bottomNavigationBar: AppNavBar(
            librarySelected: _index == 1,
            onLibrary: () => setState(() => _index = 1),
            onCamera: () {
              setState(() => _index = 0);
              _identifyKey.currentState?.openCamera();
            },
            onMenu: () => showAppMenu(context),
          ),
        ),
      ],
    );
  }
}
