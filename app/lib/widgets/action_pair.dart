import 'package:flutter/material.dart';

import '../theme/tokens.dart';

/// Two thumb-sized actions in a row, stacking when the row would overflow.
class ActionPair extends StatelessWidget {
  const ActionPair({
    super.key,
    required this.first,
    required this.second,
  });

  final Widget first;
  final Widget second;

  @override
  Widget build(BuildContext context) {
    return LayoutBuilder(
      builder: (context, constraints) {
        final stack = constraints.maxWidth < AppSpace.stackActionsBelow;
        if (stack) {
          return Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              first,
              const SizedBox(height: AppSpace.sm),
              second,
            ],
          );
        }
        return Row(
          children: [
            Expanded(child: first),
            const SizedBox(width: AppSpace.sm),
            Expanded(child: second),
          ],
        );
      },
    );
  }
}
