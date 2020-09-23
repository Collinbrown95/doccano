import os

from django.conf import settings
from django.test import override_settings
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from model_mommy import mommy

from ..models import User, SequenceAnnotation, Document, TextClassificationProject, Role, RoleMapping, DocumentFeedback
from ..models import DOCUMENT_CLASSIFICATION, SEQUENCE_LABELING, SEQ2SEQ, SPEECH2TEXT
from ..utils import PlainTextParser, CoNLLParser, JSONParser, CSVParser
from ..exceptions import FileParseException
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def create_default_roles():
    Role.objects.get_or_create(name=settings.ROLE_PROJECT_ADMIN)
    Role.objects.get_or_create(name=settings.ROLE_ANNOTATOR)
    Role.objects.get_or_create(name=settings.ROLE_ANNOTATION_APPROVER)


def assign_user_to_role(project_member, project, role_name):
    role, _ = Role.objects.get_or_create(name=role_name)
    RoleMapping.objects.get_or_create(role_id=role.id, user_id=project_member.id, project_id=project.id)


def remove_all_role_mappings():
    RoleMapping.objects.all().delete()


class DocumentFeedbackAPI(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.annotator_name = 'annotator_name'
        cls.annotator_pass = 'annotator_pass'
        cls.annotator_feedback = 'This is feedback from the annotator'
        cls.annotator_edited_feedback = 'This is EDITED feedback from the annotator'
        cls.approver_name = 'approver_name_name'
        cls.approver_pass = 'approver_pass'
        cls.approver_feedback = 'This is feedback from the approver'
        cls.project_admin_name = 'project_admin_name'
        cls.project_admin_pass = 'project_admin_pass'
        cls.project_admin_feedback = 'This is feedback from the project admin'
        # Users
        cls.annotator = User.objects.create_user(username=cls.annotator_name,
                                                 password=cls.annotator_pass)
        cls.approver = User.objects.create_user(username=cls.approver_name,
                                                password=cls.approver_pass)
        cls.project_admin = User.objects.create_user(username=cls.project_admin_name,
                                                     password=cls.project_admin_pass)
        # Project
        project = mommy.make('TextClassificationProject', users=[cls.annotator, cls.approver, cls.project_admin])
        # Document
        cls.document = mommy.make('Document', project=project)
        # URLs
        cls.feedback_url = reverse(viewname='document_feedback', args=[project.id, cls.document.id])
        cls.doclist_url = reverse(viewname='doc_list', args=[project.id])
        # User roles
        create_default_roles()
        assign_user_to_role(project_member=cls.annotator, project=project,
                            role_name=settings.ROLE_ANNOTATOR)
        assign_user_to_role(project_member=cls.approver, project=project,
                            role_name=settings.ROLE_ANNOTATION_APPROVER)
        assign_user_to_role(project_member=cls.project_admin, project=project,
                            role_name=settings.ROLE_PROJECT_ADMIN)
    
    def test_users_post_and_edit_feedback(self):
        ''' All 3 roles should be able to successfully post a feedback. '''
        # Verify there are zero feedbacks provided
        self.assertEqual(len(DocumentFeedback.objects.all()),
                         0,
                         'Expected zero feedback entries but found > 0')
        # Annotator test
        self.client.login(username=self.annotator_name,
                          password=self.annotator_pass)
        response = self.client.post(self.feedback_url,
                                    format='json',
                                    data={
                                        'text': self.annotator_feedback,
                                        'doc_id': self.document.id})
        self.assertDictEqual({
            'id': response.data['id'],
            'text': self.annotator_feedback,
            'document': self.document.id,
            'username': self.annotator_name
        },
        response.data,
        f'Expected response from {self.annotator_name} to match, but it did not.')
        self.client.logout()
        # Approver test
        self.client.login(username=self.approver_name,
                          password=self.approver_pass)
        response = self.client.post(self.feedback_url,
                                    format='json',
                                    data={
                                        'text': self.approver_feedback,
                                        'doc_id': self.document.id})
        self.assertDictEqual({
            'id': response.data['id'],
            'text': self.approver_feedback,
            'document': self.document.id,
            'username': self.approver_name
        },
        response.data,
        f'Expected response from {self.approver_name} to match, but it did not.')
        self.client.logout()
        # Project admin test
        self.client.login(username=self.project_admin_name,
                          password=self.project_admin_pass)
        response = self.client.post(self.feedback_url,
                                    format='json',
                                    data={
                                        'text': self.project_admin_feedback,
                                        'doc_id': self.document.id})
        self.assertDictEqual({
            'id': response.data['id'],
            'text': self.project_admin_feedback,
            'document': self.document.id,
            'username': self.project_admin_name
        },
        response.data,
        f'Expected response from {self.project_admin_name} to match, but it did not.')
        self.client.logout()
        # Check that a user can return to their feedback and edit it
        self.client.login(username=self.annotator_name,
                          password=self.annotator_pass)
        response = self.client.post(self.feedback_url,
                                    format='json',
                                    data={
                                      'text': self.annotator_edited_feedback,
                                      'doc_id': self.document.id})
        temp = Document.objects.all().first()
        self.assertDictEqual({
            'id': response.data['id'],
            'text': self.annotator_edited_feedback,
            'document': self.document.id,
            'username': self.annotator_name
        },
        response.data,
        f'Expected updated response from {self.annotator_name} to match, but it did not.')    
