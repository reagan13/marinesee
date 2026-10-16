import 'package:flutter/material.dart';

import '../data/profile_controller.dart';
import '../theme/tokens.dart';
import '../widgets/ocean_layout.dart';
import '../widgets/ocean_surface.dart';
import '../widgets/wash_title.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  static const purpose =
      'MarineSee identifies and teaches the nine Mati species.';

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final _name = TextEditingController();
  var _loaded = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_loaded) {
      return;
    }
    _name.text = ProfileScope.of(context).name;
    _loaded = true;
  }

  @override
  void dispose() {
    _name.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final profile = ProfileScope.of(context);
    final text = Theme.of(context).textTheme;

    return OceanScaffold(
      atmosphere: false,
      header: const WashTitle(
        title: 'Profile',
        subtitle: 'Mati City',
      ),
      body: OceanPage(
        children: [
          TextField(
            controller: _name,
            textCapitalization: TextCapitalization.words,
            textInputAction: TextInputAction.done,
            decoration: const InputDecoration(
              labelText: 'Your name',
              hintText: 'Shown on Home',
            ),
            onChanged: profile.setName,
          ),
          const SizedBox(height: 8),
          Text(
            'Stored on this device only. No account.',
            style: text.bodySmall,
          ),
          const SizedBox(height: 16),
          OceanSurface(
            child: Text(ProfileScreen.purpose, style: text.bodyLarge),
          ),
          const SizedBox(height: 16),
          const OceanSurface(
            child: Column(
              children: [
                _Step(number: '1', label: 'Camera or gallery'),
                OceanDivider(),
                _Step(number: '2', label: 'Read the name and percent'),
                OceanDivider(),
                _Step(number: '3', label: 'Open the library and 3D'),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _Step extends StatelessWidget {
  const _Step({required this.number, required this.label});

  final String number;
  final String label;

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final text = Theme.of(context).textTheme;

    return ConstrainedBox(
      constraints: const BoxConstraints(minHeight: AppTokens.tapMin),
      child: Row(
        children: [
          Container(
            width: 32,
            height: 32,
            alignment: Alignment.center,
            decoration: BoxDecoration(
              color: tokens.brandDeep,
              borderRadius: BorderRadius.circular(10),
            ),
            child: Text(
              number,
              style: text.labelLarge?.copyWith(color: tokens.onBrand),
            ),
          ),
          const SizedBox(width: 12),
          Expanded(child: Text(label, style: text.titleMedium)),
        ],
      ),
    );
  }
}
