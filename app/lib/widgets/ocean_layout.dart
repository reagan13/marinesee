import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';

import '../theme/tokens.dart';
import 'aurora_atmosphere.dart';

/// Page chrome: optional sky atmosphere, transparent scaffold, mobile-first padding.
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
    final bar = title == null
        ? null
        : AppBar(
            title: Text(title!, overflow: TextOverflow.ellipsis),
            actions: actions,
            leading: leading,
          );

    final Widget content;
    if (title != null) {
      content = body;
    } else if (header != null) {
      content = SafeArea(
        bottom: false,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Padding(
              padding: AppSpace.headerInsets(context),
              child: header,
            ),
            Expanded(child: body),
          ],
        ),
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

/// Scrollable column capped at [AppSpace.maxContent] for tablet/desktop.
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
