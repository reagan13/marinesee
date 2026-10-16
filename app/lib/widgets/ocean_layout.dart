import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../theme/tokens.dart';
import 'aurora_atmosphere.dart';

/// Page chrome: light page, curved teal header, transparent scaffold.
class OceanScaffold extends StatelessWidget {
  const OceanScaffold({
    super.key,
    required this.body,
    this.title,
    this.header,
    this.atmosphere = true,
    this.actions,
    this.leading,
  });

  final Widget body;
  final String? title;
  final Widget? header;
  final bool atmosphere;
  final List<Widget>? actions;
  final Widget? leading;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final bar = title == null
        ? null
        : AppBar(
            title: Text(title!, overflow: TextOverflow.ellipsis),
            actions: actions,
            leading: leading,
            backgroundColor: Colors.transparent,
            surfaceTintColor: Colors.transparent,
            foregroundColor: SkyPalette.onHeader,
            elevation: 0,
            scrolledUnderElevation: 0,
            iconTheme: const IconThemeData(color: SkyPalette.onHeader),
            actionsIconTheme: const IconThemeData(color: SkyPalette.onHeader),
            titleTextStyle: Theme.of(context).textTheme.titleLarge?.copyWith(
              color: SkyPalette.onHeader,
            ),
            flexibleSpace: ClipRRect(
              borderRadius: const BorderRadius.vertical(
                bottom: Radius.circular(28),
              ),
              child: DecoratedBox(
                decoration: BoxDecoration(gradient: tokens.headerGradient),
                child: const SizedBox.expand(),
              ),
            ),
          );

    final Widget content;
    if (title != null) {
      content = body;
    } else if (header != null) {
      content = Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          ClipRRect(
            borderRadius: const BorderRadius.vertical(
              bottom: Radius.circular(28),
            ),
            child: DecoratedBox(
              decoration: BoxDecoration(gradient: tokens.headerGradient),
              child: SafeArea(
                bottom: false,
                child: Padding(
                  padding: AppSpace.headerInsets(context),
                  child: header,
                ),
              ),
            ),
          ),
          Expanded(child: body),
        ],
      );
    } else {
      content = SafeArea(bottom: false, child: body);
    }

    return Stack(
      fit: StackFit.expand,
      children: [
        if (atmosphere) const AuroraAtmosphere(),
        Scaffold(
          backgroundColor: Colors.transparent,
          resizeToAvoidBottomInset: !kIsWeb,
          appBar: bar,
          body: content,
        ),
      ],
    );
  }
}

/// Scrollable column capped at [AppSpace.maxContent] for tablet width.
class OceanPage extends StatelessWidget {
  const OceanPage({
    super.key,
    required this.children,
    this.controller,
    this.extraBottom = 0,
  });

  final List<Widget> children;
  final ScrollController? controller;
  final double extraBottom;

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.topCenter,
      child: ConstrainedBox(
        constraints: const BoxConstraints(maxWidth: AppSpace.maxContent),
        child: ListView(
          controller: controller,
          padding: AppSpace.pageInsets(context, extraBottom: extraBottom),
          children: children,
        ),
      ),
    );
  }
}
