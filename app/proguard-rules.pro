# kotlinx.serialization
-keepattributes *Annotation*, InnerClasses
-keepclassmembers @kotlinx.serialization.Serializable class ** { *** Companion; *; }
-keep,includedescriptorclasses class dev.tobi.manna.**$$serializer { *; }
