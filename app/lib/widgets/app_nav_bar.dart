import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// Flat white bar. Five equal tabs, label under the icon.
class AppNavBar extends StatelessWidget {
  const AppNavBar({
    super.key,
    required this.index,
    required this.onSelect,
    this.dark = false,
  });

  final int index;
  final ValueChanged<int> onSelect;
  final bool dark;

  static const _tabs = [
    _Tab(Icons.home_outlined, Icons.home, 'Home'),
    _Tab(Icons.crop_free, Icons.crop_free, 'Scan'),
    _Tab(Icons.storage_outlined, Icons.storage, 'Library'),
    _Tab(Icons.favorite_border, Icons.favorite, 'Conservation'),
    _Tab(Icons.person_outline, Icons.person, 'Profile'),
  ];

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final bar = dark ? SkyPalette.scannerDeep : tokens.surfaceHigh;
    final line = dark ? Colors.white.withValues(alpha: 0.12) : tokens.border;

    return DecoratedBox(
      decoration: BoxDecoration(
        boxShadow: dark
            ? null
            : const [
                BoxShadow(
                  color: SkyPalette.shadow,
                  blurRadius: 18,
                  offset: Offset(0, -6),
                ),
              ],
      ),
      child: Material(
        color: bar,
        child: DecoratedBox(
          decoration: BoxDecoration(
            color: bar,
            border: Border(top: BorderSide(color: line)),
          ),
          child: SafeArea(
            top: false,
            child: SizedBox(
              height: 64,
              child: Row(
                children: [
                  for (var i = 0; i < _tabs.length; i++)
                    Expanded(
                      child: _NavTab(
                        tab: _tabs[i],
                        selected: index == i,
                        dark: dark,
                        onTap: () => onSelect(i),
                      ),
                    ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}

class _Tab {
  const _Tab(this.icon, this.selectedIcon, this.label);

  final IconData icon;
  final IconData selectedIcon;
  final String label;
}

class _NavTab extends StatelessWidget {
  const _NavTab({
    required this.tab,
    required this.selected,
    required this.dark,
    required this.onTap,
  });

  final _Tab tab;
  final bool selected;
  final bool dark;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final color = selected
        ? (dark ? SkyPalette.foam : SkyPalette.primaryDark)
        : (dark ? Colors.white.withValues(alpha: 0.72) : tokens.inkMuted);

    return Tooltip(
      message: tab.label,
      child: Semantics(
        button: true,
        selected: selected,
        label: tab.label,
        child: InkWell(
          onTap: onTap,
          child: SizedBox(
            height: 64,
            child: FittedBox(
              fit: BoxFit.scaleDown,
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Container(
                    width: 32,
                    height: 32,
                    alignment: Alignment.center,
                    decoration: BoxDecoration(
                      color: selected ? tokens.brand : Colors.transparent,
                      shape: BoxShape.circle,
                    ),
                    child: Icon(
                      selected ? tab.selectedIcon : tab.icon,
                      size: 22,
                      color: selected
                          ? tokens.onBrand
                          : (dark
                                ? Colors.white.withValues(alpha: 0.72)
                                : tokens.inkMuted),
                    ),
                  ),
                  const SizedBox(height: 2),
                  Text(
                    tab.label,
                    maxLines: 1,
                    style: Theme.of(context).textTheme.labelSmall?.copyWith(
                      fontSize: 11,
                      fontWeight: selected ? FontWeight.w700 : FontWeight.w500,
                      color: color,
                    ),
                  ),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
