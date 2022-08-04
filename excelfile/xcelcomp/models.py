from django.db import models
from django.core.files import File
from io import BytesIO
import pandas as pd
# Create your models here.


class ExcelFiles(models.Model):
    title = models.CharField(max_length=100)
    excel = models.FileField(upload_to='excels', blank=True, null=True)
    duplicates_file = models.FileField(
        upload_to='duplicate', blank=True, null=True)
    duplicate_free = models.FileField(
        upload_to='duplifree', blank=True, null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.get_duplicate_free = self.make_duplicate_free(self.excel)
        self.get_duplicates_file = self.make_duplicates_file(self.excel)
        return super().save(*args, **kwargs)

    def get_excel(self):
        if self.excel:
            return self.excel

    def get_duplicate_free(self):
        if self.duplicate_free:
            return self.duplicate_free
        else:
            if self.excel:
                self.duplicate_free = self.make_duplicate_free(self.excel)
                self.save()
                return self.duplicate_free
            else:
                return ''

    def make_duplicate_free(self, excel):
        excel_doc = pd.read_excel(excel)
        excel_doc.drop_duplicates()
        df = excel_doc.to_excel(
            'duplicate_free.xlsx', index=False)

        return df

    def get_duplicates_file(self):
        if self.duplicates_file:
            return self.duplicates_file
        else:
            if self.excel:
                self.duplicates_file = self.make_duplicates_file(self.excel)
                self.save()
                return self.duplicates_file
            else:
                return ''

    def make_duplicates_file(self, excel):  # for highlighting duplicates blue
        excel_docs = pd.read_excel(excel)
        excel_docs.duplicated(keep=False)
        docs = excel_docs[excel_docs].index.values
        excel_docs.style.apply(
            lambda x: ['background: blue' if x.name in docs else '' for i in x], axis=1)
        duplicates_free = excel_docs.to_excel(
            'duplicates_free.xlsx', index=False)
        return duplicates_free


# from io import BytesIO
# bio = BytesIO()
# # By setting the 'engine' in the ExcelWriter constructor.
# writer = pd.ExcelWriter(bio, engine="xlsxwriter")
# df.to_excel(writer, sheet_name="Sheet1")
# # Save the workbook
# writer.save()
# # Seek to the beginning and read to copy the workbook to a variable in memory
# bio.seek(0)
# workbook = bio.read()
# import zipfile
# >>> df = pd.DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
# >>> with zipfile.ZipFile("path_to_file.zip", "w") as zf:
# ... with zf.open("filename.xlsx", "w") as buffer:
# ... with pd.ExcelWriter(buffer) as writer:
# ... df.to_excel(writer)
# >> > import io
# >> > df = pd.DataFrame([["ABC", "XYZ"]], columns=["Foo", "Bar"])
# >> > buffer = io.BytesIO()
# >> > with pd.ExcelWriter(buffer) as writer:
# ... df.to_excel(writer)
