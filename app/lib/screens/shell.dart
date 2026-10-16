import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

import '../classify/api_classifier.dart';
import '../theme/tokens.dart';
import '../widgets/app_nav_bar.dart';
import '../widgets/aurora_atmosphere.dart';
import 'conservation_screen.dart';
import 'home_screen.dart';
import 'identify_screen.dart';
import 'library_screen.dart';
import 'profile_screen.dart';
import 'shell_scope.dart';

class AppShell extends StatefulWidget {
  const AppShell({super.key});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  var _index = ShellTab.home;
  final _classifier = ApiClassifier();

  void _select(int index) => setState(() => _index = index);

  @override
  Widget build(BuildContext context) {
    final pages = [
      const HomeScreen(),
      IdentifyScreen(classifier: _classifier),
      const LibraryScreen(),
      const ConservationScreen(),
      const ProfileScreen(),
    ];

    final scan = _index == ShellTab.scan;

    return ShellScope(
      select: _select,
      child: AnnotatedRegion<SystemUiOverlayStyle>(
        value: scan ? SkyPalette.lightStatusBar : SkyPalette.headerStatusBar,
        child: Stack(
          fit: StackFit.expand,
          children: [
            const AuroraAtmosphere(),
            Scaffold(
              backgroundColor: Colors.transparent,
              resizeToAvoidBottomInset: !kIsWeb,
              body: IndexedStack(
                index: _index,
                children: [
                  for (var i = 0; i < pages.length; i++)
                    TickerMode(enabled: i == _index, child: pages[i]),
                ],
              ),
              bottomNavigationBar: AppNavBar(
                index: _index,
                onSelect: _select,
                dark: scan,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
