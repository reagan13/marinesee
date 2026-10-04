import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';

import '../classify/classifier.dart';
import '../data/profile_controller.dart';
import '../theme/tokens.dart';
import '../widgets/action_pair.dart';
import '../widgets/app_header.dart';
import '../widgets/aurora_button.dart';
import '../widgets/ocean_layout.dart';
import '../widgets/ocean_surface.dart';
import '../widgets/profile_avatar.dart';
import 'profile_settings_screen.dart';
import 'result_screen.dart';

class IdentifyScreen extends StatefulWidget {
  const IdentifyScreen({super.key, required this.classifier});

  final Classifier classifier;

  @override
  @override
  IdentifyScreenState createState() => IdentifyScreenState();
}

class IdentifyScreenState extends State<IdentifyScreen> {
  final _picker = ImagePicker();
  XFile? _image;
  Uint8List? _bytes;
  bool _busy = false;

  Future<void> openCamera() => _pick(ImageSource.camera);

  Future<void> _pick(ImageSource source) async {
    try {
      final picked = await _picker.pickImage(source: source);
      if (picked == null) {
        return;
      }
      final bytes = await picked.readAsBytes();
      setState(() {
        _image = picked;
        _bytes = bytes;
      });
    } catch (error) {
      if (!mounted) {
        return;
      }
      final message = error is PlatformException
          ? (error.message ?? 'Could not open the camera or gallery.')
          : 'Could not open the camera or gallery.';
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(message)));
    }
  }

  Future<void> _identify() async {
    final image = _image;
    if (image == null || _busy) {
      return;
    }
    setState(() => _busy = true);
    final result = await widget.classifier.identify(image);
    if (!mounted) {
      return;
    }
    setState(() => _busy = false);
    await Navigator.of(context).push(
      MaterialPageRoute<void>(
        builder: (_) => ResultScreen(imageBytes: _bytes!, result: result),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final profile = ProfileScope.of(context);

    return OceanScaffold(
      atmosphere: false,
      header: AppHeader(
        greeting: 'Hello, ${profile.displayName}',
        title: 'Find a seagrass',
        place: 'Mati City, Davao Oriental',
        trailing: ProfileAvatar(
          initials: profile.initials,
          photoBytes: profile.photoBytes,
          size: 44,
          onTap: () {
            Navigator.of(context).push(
              MaterialPageRoute<void>(
                builder: (_) => const ProfileSettingsScreen(),
              ),
            );
          },
        ),
      ),
      body: OceanPage(
        extraBottom: AppSpace.navClearance,
        children: [
          _Preview(bytes: _bytes),
          const SizedBox(height: 18),
          ActionPair(
            first: OutlinedButton.icon(
              onPressed: () => _pick(ImageSource.camera),
              icon: const Icon(Icons.photo_camera_outlined),
              label: const Text('Camera'),
            ),
            second: OutlinedButton.icon(
              onPressed: () => _pick(ImageSource.gallery),
              icon: const Icon(Icons.photo_library_outlined),
              label: const Text('Gallery'),
            ),
          ),
          const SizedBox(height: 16),
          AuroraButton(
            label: _busy ? 'Identifying…' : 'Identify',
            icon: Icons.auto_awesome_outlined,
            loading: _busy,
            onPressed: _image == null || _busy ? null : _identify,
          ),
        ],
      ),
    );
  }
}

class _Preview extends StatelessWidget {
  const _Preview({required this.bytes});

  final Uint8List? bytes;

  @override
  Widget build(BuildContext context) {
    final text = Theme.of(context).textTheme;
    final tokens = context.tokens;

    if (bytes == null) {
      return OceanSurface(
        glow: true,
        height: 280,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              width: 72,
              height: 72,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: tokens.surfaceHigh.withValues(alpha: 0.88),
                border: Border.all(color: tokens.brand.withValues(alpha: 0.35), width: 1.4),
                boxShadow: tokens.glowShadows,
              ),
              child: Icon(Icons.spa_outlined, size: 32, color: tokens.brand),
            ),
            const SizedBox(height: 16),
            Text('No photo yet', style: text.titleMedium),
            const SizedBox(height: 6),
            Text(
              'Camera or gallery, then identify the leaf.',
              textAlign: TextAlign.center,
              style: text.bodySmall,
            ),
          ],
        ),
      );
    }

    return OceanSurface(
      glow: true,
      padding: EdgeInsets.zero,
      height: 280,
      child: Image.memory(
        bytes!,
        fit: BoxFit.cover,
        width: double.infinity,
        height: 280,
      ),
    );
  }
}
