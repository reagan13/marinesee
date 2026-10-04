import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:image_picker/image_picker.dart';

import '../data/profile_controller.dart';
import '../theme/tokens.dart';
import '../widgets/action_pair.dart';
import '../widgets/aurora_button.dart';
import '../widgets/ocean_layout.dart';
import '../widgets/ocean_surface.dart';
import '../widgets/profile_avatar.dart';
import '../widgets/section_header.dart';

class ProfileSettingsScreen extends StatefulWidget {
  const ProfileSettingsScreen({super.key});

  @override
  State<ProfileSettingsScreen> createState() => _ProfileSettingsScreenState();
}

class _ProfileSettingsScreenState extends State<ProfileSettingsScreen> {
  final _first = TextEditingController();
  final _last = TextEditingController();
  final _picker = ImagePicker();
  Uint8List? _photo;
  var _loaded = false;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (_loaded) {
      return;
    }
    final profile = ProfileScope.of(context);
    _first.text = profile.firstName;
    _last.text = profile.lastName;
    _photo = profile.photoBytes;
    _loaded = true;
  }

  @override
  void dispose() {
    _first.dispose();
    _last.dispose();
    super.dispose();
  }

  Future<void> _pick(ImageSource source) async {
    try {
      final picked = await _picker.pickImage(
        source: source,
        maxWidth: 720,
        imageQuality: 85,
      );
      if (picked == null) {
        return;
      }
      final bytes = await picked.readAsBytes();
      setState(() => _photo = bytes);
    } on PlatformException catch (error) {
      if (!mounted) {
        return;
      }
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(
            error.message ?? 'Could not open the camera or gallery.',
          ),
        ),
      );
    }
  }

  void _save() {
    ProfileScope.of(context).save(
      firstName: _first.text,
      lastName: _last.text,
      photoBytes: _photo,
    );
    Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    final tokens = context.tokens;
    final first = _first.text.trim();
    final last = _last.text.trim();
    final initials = '${first.isEmpty ? '' : first[0]}'
            '${last.isEmpty ? '' : last[0]}'
        .toUpperCase();

    return OceanScaffold(
      title: 'Profile settings',
      body: OceanPage(
        children: [
          const SectionHeader(title: 'Photo'),
          const SizedBox(height: 10),
          OceanSurface(
            child: Column(
              children: [
                ProfileAvatar(
                  initials: initials.isEmpty ? '?' : initials,
                  photoBytes: _photo,
                  size: 104,
                ),
                const SizedBox(height: 16),
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
                if (_photo != null) ...[
                  const SizedBox(height: 8),
                  TextButton(
                    onPressed: () => setState(() => _photo = null),
                    child: const Text('Remove photo'),
                  ),
                ],
              ],
            ),
          ),
          const SizedBox(height: 22),
          const SectionHeader(title: 'Name'),
          const SizedBox(height: 10),
          OceanSurface(
            child: Column(
              children: [
                TextField(
                  controller: _first,
                  textCapitalization: TextCapitalization.words,
                  textInputAction: TextInputAction.next,
                  decoration: const InputDecoration(
                    labelText: 'First name',
                    hintText: 'e.g. Daisy',
                  ),
                  onChanged: (_) => setState(() {}),
                ),
                const SizedBox(height: 14),
                TextField(
                  controller: _last,
                  textCapitalization: TextCapitalization.words,
                  textInputAction: TextInputAction.done,
                  decoration: const InputDecoration(
                    labelText: 'Last name',
                    hintText: 'e.g. Reyes',
                  ),
                  onChanged: (_) => setState(() {}),
                ),
              ],
            ),
          ),
          const SizedBox(height: 10),
          Text(
            'Stored on this device only. No visitor login in this build.',
            style: Theme.of(context).textTheme.bodySmall?.copyWith(
              color: tokens.inkSubtle,
            ),
          ),
          const SizedBox(height: 22),
          AuroraButton(
            label: 'Save',
            icon: Icons.check,
            onPressed: _save,
          ),
          const SizedBox(height: 12),
          OutlinedButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
        ],
      ),
    );
  }
}
