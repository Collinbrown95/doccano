from django.test import TestCase, override_settings
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from model_mommy import mommy

from ..models import Label, DocumentAnnotation, SequenceAnnotation, Seq2seqAnnotation, Speech2textAnnotation
from ..models import Document, User, DocumentFeedback
from ..serializers import DocumentAnnotationSerializer
from ..serializers import SequenceAnnotationSerializer
from ..serializers import Seq2seqAnnotationSerializer
from ..serializers import Speech2textAnnotationSerializer


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestTextClassificationProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = mommy.make('TextClassificationProject')

    def test_image(self):
        image_url = self.project.image
        self.assertTrue(image_url.endswith('.jpg'))

    def test_get_bundle_name(self):
        template = self.project.get_bundle_name()
        self.assertEqual(template, 'document_classification')

    def test_get_annotation_serializer(self):
        serializer = self.project.get_annotation_serializer()
        self.assertEqual(serializer, DocumentAnnotationSerializer)

    def test_get_annotation_class(self):
        klass = self.project.get_annotation_class()
        self.assertEqual(klass, DocumentAnnotation)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestSequenceLabelingProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = mommy.make('SequenceLabelingProject')

    def test_image(self):
        image_url = self.project.image
        self.assertTrue(image_url.endswith('.jpg'))

    def test_get_bundle_name(self):
        template = self.project.get_bundle_name()
        self.assertEqual(template, 'sequence_labeling')

    def test_get_annotation_serializer(self):
        serializer = self.project.get_annotation_serializer()
        self.assertEqual(serializer, SequenceAnnotationSerializer)

    def test_get_annotation_class(self):
        klass = self.project.get_annotation_class()
        self.assertEqual(klass, SequenceAnnotation)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestSeq2seqProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = mommy.make('Seq2seqProject')

    def test_image(self):
        image_url = self.project.image
        self.assertTrue(image_url.endswith('.jpg'))

    def test_get_bundle_name(self):
        template = self.project.get_bundle_name()
        self.assertEqual(template, 'seq2seq')

    def test_get_annotation_serializer(self):
        serializer = self.project.get_annotation_serializer()
        self.assertEqual(serializer, Seq2seqAnnotationSerializer)

    def test_get_annotation_class(self):
        klass = self.project.get_annotation_class()
        self.assertEqual(klass, Seq2seqAnnotation)


@override_settings(STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage')
class TestSpeech2textProject(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.project = mommy.make('Speech2textProject')

    def test_image(self):
        image_url = self.project.image
        self.assertTrue(image_url.endswith('.jpg'))

    def test_get_bundle_name(self):
        template = self.project.get_bundle_name()
        self.assertEqual(template, 'speech2text')

    def test_get_annotation_serializer(self):
        serializer = self.project.get_annotation_serializer()
        self.assertEqual(serializer, Speech2textAnnotationSerializer)

    def test_get_annotation_class(self):
        klass = self.project.get_annotation_class()
        self.assertEqual(klass, Speech2textAnnotation)


class TestLabel(TestCase):

    def test_text_uniqueness(self):
        label = mommy.make('Label')
        mommy.make('Label', text=label.text)
        with self.assertRaises(IntegrityError):
            Label(project=label.project, text=label.text).save()

    def test_keys_uniqueness(self):
        label = mommy.make('Label', prefix_key='ctrl', suffix_key='a')
        with self.assertRaises(ValidationError):
            Label(project=label.project,
                  text='example',
                  prefix_key=label.prefix_key,
                  suffix_key=label.suffix_key).full_clean()

    def test_suffix_key_uniqueness(self):
        label = mommy.make('Label', prefix_key=None, suffix_key='a')
        with self.assertRaises(ValidationError):
            Label(project=label.project,
                  text='example',
                  prefix_key=label.prefix_key,
                  suffix_key=label.suffix_key).full_clean()

    def test_cannot_add_label_only_prefix_key(self):
        project = mommy.make('Project')
        label = Label(project=project,
                      text='example',
                      prefix_key='ctrl')
        with self.assertRaises(ValidationError):
            label.clean()

    def test_can_add_label_only_suffix_key(self):
        project = mommy.make('Project')
        label = Label(project=project,
                      text='example',
                      suffix_key='a')
        label.full_clean()

    def test_can_add_label_suffix_key_with_prefix_key(self):
        project = mommy.make('Project')
        label = Label(project=project,
                      text='example',
                      prefix_key='ctrl',
                      suffix_key='a')
        label.full_clean()


class TestDocumentAnnotation(TestCase):

    def test_uniqueness(self):
        a = mommy.make('DocumentAnnotation')
        with self.assertRaises(IntegrityError):
            DocumentAnnotation(document=a.document, user=a.user, label=a.label).save()


class TestSequenceAnnotation(TestCase):

    def test_uniqueness(self):
        a = mommy.make('SequenceAnnotation')
        with self.assertRaises(IntegrityError):
            SequenceAnnotation(document=a.document,
                               user=a.user,
                               label=a.label,
                               start_offset=a.start_offset,
                               end_offset=a.end_offset).save()

    def test_position_constraint(self):
        with self.assertRaises(ValidationError):
            mommy.make('SequenceAnnotation',
                       start_offset=1, end_offset=0).clean()


class TestSeq2seqAnnotation(TestCase):

    def test_uniqueness(self):
        a = mommy.make('Seq2seqAnnotation')
        with self.assertRaises(IntegrityError):
            Seq2seqAnnotation(document=a.document,
                              user=a.user,
                              text=a.text).save()


class TestDocumentFeedback(TestCase):
    '''
    Testing that the DocumentFeedback model does CRUD operations as expected.
    '''
    @classmethod
    def setUpTestData(cls):
        cls.annotator_name = 'annotator_name'
        cls.annotator_pass = 'annotator_pass'
        cls.approver_name = 'approver_name_name'
        cls.approver_pass = 'approver_pass'
        cls.project_admin_name = 'project_admin_name'
        cls.project_admin_pass = 'project_admin_pass'
        cls.annotator = User.objects.create_user(username=cls.annotator_name,
                                                 password=cls.annotator_pass)
        cls.approver = User.objects.create_user(username=cls.approver_name,
                                                password=cls.approver_pass)
        cls.project_admin = User.objects.create_user(username=cls.project_admin_name,
                                                     password=cls.project_admin_pass)
        cls.project = mommy.make('TextClassificationProject', users=[cls.annotator,
                                                                     cls.approver,
                                                                     cls.project_admin])
        cls.document = mommy.make('Document', project=cls.project)

    def test_multiple_feedbacks_write_by_object_reference_successfully(self):
        self.assertEqual(len(DocumentFeedback.objects.all()),
                         0,
                         f'Expected zero feedback entries but found {len(DocumentFeedback.objects.all())}.')
        annotator_feedback = mommy.make('DocumentFeedback',
                                        document=self.document,
                                        user=self.annotator)
        approver_feedback = mommy.make('DocumentFeedback',
                                       document=self.document,
                                       user=self.approver)
        project_admin_feedback = mommy.make('DocumentFeedback',
                                            document=self.document,
                                            user=self.project_admin)
        self.assertEqual(len(DocumentFeedback.objects.all()),
                         3,
                         f'Expected three feedback entries, but found {len(DocumentFeedback.objects.all())}.')

    def test_multiple_feedbacks_write_by_id_successfully(self):
        self.assertEqual(len(DocumentFeedback.objects.all()),
                         0,
                         f'Expected zero feedback entries but found {len(DocumentFeedback.objects.all())}.')
        annotator_feedback = mommy.make('DocumentFeedback',
                                        document_id=self.document.id,
                                        user_id=self.annotator.id)
        approver_feedback = mommy.make('DocumentFeedback',
                                       document_id=self.document.id,
                                       user_id=self.approver.id)
        project_admin_feedback = mommy.make('DocumentFeedback',
                                            document_id=self.document.id,
                                            user_id=self.project_admin.id)
        self.assertEqual(len(DocumentFeedback.objects.all()),
                         3,
                         f'Expected three feedback entries, but found {len(DocumentFeedback.objects.all())}.')
    
    def test_read_feedback_successfully(self):
        annotator_feedback = mommy.make('DocumentFeedback',
                                        document=self.document,
                                        user=self.annotator)
        self.assertEqual(len(DocumentFeedback.objects.all()),
                         1,
                         f'Expected one feedback entry but found {len(DocumentFeedback.objects.all())}.')
        self.assertEqual(DocumentFeedback.objects.filter(user_id=self.annotator.id)[0].user,
                         self.annotator,
                         'Expected users to match, but they did not.')
    
    def test_update_feedback_successfully(self):
        new_feedback = 'Updated text with a new edit'
        annotator_feedback = mommy.make('DocumentFeedback',
                                        document=self.document,
                                        user=self.annotator)
        self.assertEqual(len(DocumentFeedback.objects.all()),
                         1,
                         f'Expected one feedback entry but found {len(DocumentFeedback.objects.all())}.')
        annotator_feedback.text = new_feedback
        annotator_feedback.save()
        updated_feedback = DocumentFeedback.objects.filter(user=self.annotator)[0]
        self.assertEqual(updated_feedback.text,
                         new_feedback,
                         'Expected feedback to have updated but it did not.')
    
    def test_delete_feedback_successfully(self):
        annotator_feedback = mommy.make('DocumentFeedback',
                                        document=self.document,
                                        user=self.annotator)
        self.assertEqual(len(DocumentFeedback.objects.all()),
                         1,
                         f'Expected one feedback entry but found {len(DocumentFeedback.objects.all())}.')
        DocumentFeedback.objects.filter(user=self.annotator).delete()
        self.assertEqual(len(DocumentFeedback.objects.all()),
                         0,
                         f'Expected zero feedback entries but found {len(DocumentFeedback.objects.all())}.')
